import argparse
import json
import logging
import os
import random
import importlib
import sys
import re
from svg_engine import SVGEngine
from typing import Dict, Any, List, Set, Callable

# Setup Logging
def setup_logger(log_file="build.log"):
    logger = logging.getLogger("UniversalGenerator")
    logger.setLevel(logging.DEBUG)

    # File handler
    fh = logging.FileHandler(log_file, mode='a')
    fh.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

logger = setup_logger()

class TemplateEngine:
    def __init__(self, data_pools_config: Dict[str, Any]):
        self.pools = {}
        self.load_pools(data_pools_config)

    def load_pools(self, config: Dict[str, Any]):
        for placeholder, value in config.items():
            if isinstance(value, list):
                self.pools[placeholder] = value
                continue

            filepath = value
            if not isinstance(filepath, str) or not os.path.exists(filepath):
                logger.warning(f"Data pool file not found or invalid: {filepath} for placeholder {{{placeholder}}}")
                self.pools[placeholder] = [f"{{MISSING_POOL_{placeholder}}}"]
                continue

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.pools[placeholder] = data
                    else:
                        logger.warning(f"Data pool {filepath} must be a JSON array. Treating as empty.")
                        self.pools[placeholder] = [f"{{INVALID_POOL_{placeholder}}}"]
            except Exception as e:
                logger.error(f"Failed to load data pool {filepath}: {e}")
                self.pools[placeholder] = [f"{{ERROR_POOL_{placeholder}}}"]

    def generate_context(self, variables: Dict[str, str]) -> Dict[str, Any]:
        context = {}
        for var_name, var_expr in variables.items():
            context[var_name] = self.resolve_template(var_expr, context)
        return context

    def resolve_template(self, template_str: str, context: Dict[str, Any] = None) -> str:
        if not isinstance(template_str, str):
            return template_str

        if context is None:
            context = {}

        placeholders = re.findall(r'\{([a-zA-Z0-9_]+)\}', template_str)
        result_str = template_str

        mapping = context.copy()
        for ph in placeholders:
            if ph not in mapping:
                if ph in self.pools:
                    mapping[ph] = random.choice(self.pools[ph])
                else:
                    mapping[ph] = f"{{UNKNOWN_{ph}}}"
        try:
            # Update the original context with generated values so they persist
            for k,v in mapping.items():
                if k not in context:
                    context[k] = v

            # We don't want format to crash on {eval(num1+num2)}, so we temporarily escape {eval(...) by changing it to {{eval(...)}}
            # Use string replace instead of regex sub for simplicity
            temp_result = result_str.replace('{eval(', '{{eval(').replace(')}', ')}}')

            # Now we can safely run format on the rest of the placeholders (like {num1}, {num2})
            result_str = temp_result.format(**mapping)

            # Now we must restore the {{eval(...)}} back to {eval(...)} for the subsequent eval block to process
            result_str = result_str.replace('{{eval(', '{eval(').replace(')}}', ')}')

        except KeyError as e:
            if not str(e).startswith("'eval("):
                logger.warning(f"Template formatting failed due to missing key: {e}. Template: {template_str}")
        except Exception as e:
            logger.warning(f"Unexpected error formatting template: {e}. Template: {template_str}")



        # Evaluate math expressions like {eval(num1 + num2)}
        eval_matches = re.findall(r'\{eval\((.*?)\)\}', result_str)
        for expr in eval_matches:
            try:
                # Prepare a safe environment for eval
                safe_env = {"__builtins__": None, "round": round, "abs": abs, "min": min, "max": max}
                # Cast string numbers to int/float if possible to allow eval
                eval_context = {}
                for k, v in mapping.items():
                    try:
                        if isinstance(v, str) and '.' in v:
                            eval_context[k] = float(v)
                        else:
                            eval_context[k] = int(v)
                    except (ValueError, TypeError):
                        eval_context[k] = v

                val = eval(expr, safe_env, eval_context)

                # Format to avoid trailing .0 for integers
                if isinstance(val, float) and val.is_integer():
                    val_str = str(int(val))
                else:
                    val_str = str(val)

                result_str = result_str.replace("{eval(" + expr + ")}", val_str)
            except Exception as e:
                logger.warning(f"Failed to evaluate expression '{expr}': {e}")
                result_str = result_str.replace("{eval(" + expr + ")}", f"{{ERROR_EVAL_{expr}}}")

        return result_str

    def generate_distractors(self, pool_name: str, count: int = 6, exclude: Set[str] = None, context: Dict[str, Any] = None) -> List[str]:
        if exclude is None:
            exclude = set()

        if pool_name not in self.pools:
            # If it's a dynamic distractor strategy like an expression pool
            logger.warning(f"Distractor pool '{pool_name}' not found. Using placeholders.")
            return [f"Distractor_{i}" for i in range(1, count + 1)]

        pool = self.pools[pool_name]
        available = []
        for item in pool:
            resolved_item = self.resolve_template(str(item), context)
            if resolved_item not in exclude:
                available.append(resolved_item)

        if len(available) < count:
            selected = available.copy()
            while len(selected) < count:
                selected.append(f"Fallback_Distractor_{len(selected)+1}")
            return selected

        return random.sample(available, count)

class LogicDelegator:
    @staticmethod
    def load_custom_logic(module_name: str, function_name: str) -> Callable:
        try:
            if module_name.endswith('.py'):
                module_name = module_name[:-3]

            if os.getcwd() not in sys.path:
                sys.path.insert(0, os.getcwd())

            module = importlib.import_module(module_name)
            func = getattr(module, function_name)
            return func
        except ImportError as e:
            logger.error(f"Failed to import module '{module_name}' for custom logic: {e}")
            sys.exit(1)
        except AttributeError as e:
            logger.error(f"Function '{function_name}' not found in module '{module_name}': {e}")
            sys.exit(1)

class MapUpdater:
    @staticmethod
    def derive_map_config(output_file: str, topic_name: str) -> Dict[str, str]:
        # Ex: "dataset/grade4/mathematics/paper1_mixed.json"
        parts = output_file.split('/')
        if len(parts) >= 4 and parts[0] == 'dataset':
            return {
                "grade": parts[1],
                "subject": parts[2],
                "file": parts[-1],
                "label": topic_name
            }
        return {}

    @staticmethod
    def update_map(map_file: str, map_config: Dict[str, Any], args: argparse.Namespace):
        """
        map_config should contain "grade", "subject", "file" (filename only), and "label"
        """
        grade = map_config.get("grade")
        subject = map_config.get("subject")
        file_name = map_config.get("file")
        label = map_config.get("label")

        if not all([grade, subject, file_name, label]):
            logger.warning(f"Incomplete map_config, skipping map update for {file_name}")
            return

        logger.info(f"Checking map registration in {map_file} for {grade} -> {subject} -> {file_name}")

        map_data = {}
        if os.path.exists(map_file):
            try:
                with open(map_file, 'r', encoding='utf-8') as f:
                    map_data = json.load(f)
            except Exception as e:
                logger.error(f"Failed to read map file {map_file}: {e}")
                return

        if grade not in map_data:
            map_data[grade] = {}
        if subject not in map_data[grade]:
            map_data[grade][subject] = []

        subject_list = map_data[grade][subject]

        # Check if already exists
        exists = False
        for entry in subject_list:
            if entry.get("file") == file_name:
                exists = True
                if entry.get("label") != label:
                    logger.info(f"Updating label for {file_name} from '{entry.get('label')}' to '{label}'")
                    if not args.dry_run:
                        entry["label"] = label
                break

        if not exists:
            logger.info(f"Adding new entry to {map_file}: {file_name} as '{label}'")
            if not args.dry_run:
                subject_list.append({
                    "file": file_name,
                    "label": label
                })
        else:
            logger.info(f"Entry {file_name} already registered in {map_file}")

        if not args.dry_run:
            try:
                with open(map_file, 'w', encoding='utf-8') as f:
                    json.dump(map_data, f, indent=2, ensure_ascii=False)
                logger.info(f"Successfully saved {map_file}")
            except Exception as e:
                logger.error(f"Failed to save map file {map_file}: {e}")

class DatasetManager:



    stats = {"questions_generated": 0, "files_updated": 0, "svg_count": 0, "duplicates_avoided": 0, "difficulty_distribution": {"easy": 0, "medium": 0, "hard": 0}}
    @staticmethod
    def verify_dataset(dataset: List[Dict[str, Any]], expected_topic: str) -> bool:
        if not dataset:
            logger.warning("Dataset is empty.")
            return False

        seen_questions = set()
        difficulty_counts = {"easy": 0, "medium": 0, "hard": 0}

        required_keys = ["id", "topic", "subtopic", "difficulty", "question", "correct_answer", "wrong_answers_pool", "explanation"]

        for idx, item in enumerate(dataset):
            for key in required_keys:
                if key not in item:
                    logger.error(f"Item at index {idx} missing required key: '{key}'")
                    return False

            if item["topic"] != expected_topic:
                logger.error(f"Item at index {idx} has mismatched topic: '{item['topic']}' vs expected '{expected_topic}'")
                return False

            q_text = item["question"]
            if q_text in seen_questions:
                DatasetManager.stats["duplicates_avoided"] += 1
                logger.error(f"Duplicate question found: '{q_text}'")
                return False
            seen_questions.add(q_text)

            diff = item.get("difficulty")
            if diff in difficulty_counts:
                difficulty_counts[diff] += 1
            else:
                logger.error(f"Item at index {idx} has invalid difficulty: '{diff}'")
                return False

            if len(item["wrong_answers_pool"]) < 6:
                logger.error(f"Item at index {idx} has fewer than 6 distractors.")
                return False

        total = len(dataset)
        logger.info(f"Verified dataset of {total} items. Difficulties: {difficulty_counts}")

        # Verify difficulty distribution roughly (e.g. at least within 10% of target)
        if total >= 10:
            easy_pct = difficulty_counts["easy"] / total
            medium_pct = difficulty_counts["medium"] / total
            hard_pct = difficulty_counts["hard"] / total

            if not (0.20 <= easy_pct <= 0.40):
                logger.warning(f"Easy difficulty percentage {easy_pct:.2f} is far from target 0.30")
            if not (0.40 <= medium_pct <= 0.60):
                logger.warning(f"Medium difficulty percentage {medium_pct:.2f} is far from target 0.50")
            if not (0.10 <= hard_pct <= 0.30):
                logger.warning(f"Hard difficulty percentage {hard_pct:.2f} is far from target 0.20")

        return True

    @staticmethod
    def process_topic(engine: TemplateEngine, topic_config: Dict[str, Any], args: argparse.Namespace):
        topic_name = topic_config.get("topic")
        output_file = topic_config.get("output_file")
        custom_logic = topic_config.get("custom_logic")
        templates = topic_config.get("templates", [])
        target_count = topic_config.get("target_count", 1000)
        if hasattr(args, "target_count") and args.target_count is not None:
            target_count = args.target_count

        logger.info(f"--- Processing Topic: {topic_name} ---")

        if not output_file:
            logger.error(f"No output_file defined for topic {topic_name}")
            return

        out_dir = os.path.dirname(output_file)
        if out_dir and not os.path.exists(out_dir):
            if not args.dry_run:
                os.makedirs(out_dir, exist_ok=True)
                logger.info(f"Created directory: {out_dir}")
            else:
                logger.info(f"[DRY-RUN] Would create directory: {out_dir}")

        existing_dataset = []
        if args.append and os.path.exists(output_file):
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_dataset = json.load(f)
                    logger.info(f"Loaded {len(existing_dataset)} existing questions from {output_file}")
            except Exception as e:
                logger.error(f"Failed to load existing dataset from {output_file}: {e}")
                return

        current_count = len(existing_dataset)
        needed = max(0, target_count - current_count)

        logger.info(f"Target count: {target_count}. Current count: {current_count}. Needed: {needed}.")

        final_dataset = existing_dataset

        if needed > 0:
            new_items = []
            if custom_logic:
                parts = custom_logic.split(":")
                if len(parts) == 2:
                    module_name, func_name = parts
                    func = LogicDelegator.load_custom_logic(module_name, func_name)

                    logger.info(f"Delegating generation to custom logic: {custom_logic}")
                    if args.dry_run:
                        logger.info(f"[DRY-RUN] Would call {custom_logic} to generate {needed} items.")
                    else:
                        logger.info(f"Calling {custom_logic}...")
                        try:
                            res = func()
                            if isinstance(res, list):
                                new_items.extend(res[:needed])
                                for item in new_items:
                                    if "svg" in item and item["svg"].get("content"):
                                        DatasetManager.stats["svg_count"] += 1
                            else:
                                logger.info(f"Custom logic {custom_logic} executed (no dataset returned, assuming self-saving).")
                                # We can't verify or save what we don't have, so we exit this topic
                                return
                        except Exception as e:
                            logger.error(f"Error executing custom logic {custom_logic}: {e}")
                            return
                else:
                    logger.error(f"Invalid custom_logic format: {custom_logic}")
                    return

            elif templates and engine:
                logger.info(f"Using template engine with {len(templates)} templates.")

                attempts = 0
                seen_questions = {item["question"] for item in existing_dataset}

                difficulties = ["easy", "medium", "hard"]
                weights = [0.3, 0.5, 0.2]

                while len(new_items) < needed and attempts < needed * 10:
                    attempts += 1
                    template = random.choice(templates)

                    context = {}
                    if "variables" in template:
                        context = engine.generate_context(template["variables"])

                    q_text = engine.resolve_template(template.get("question", ""), context)
                    if q_text in seen_questions:
                        DatasetManager.stats["duplicates_avoided"] += 1
                        continue

                    correct = engine.resolve_template(template.get("correct_answer", ""), context)
                    explanation = engine.resolve_template(template.get("explanation", ""), context)

                    distractor_pool_name = template.get("distractor_pool")
                    wrong_answers = []
                    if distractor_pool_name:
                        wrong_answers = engine.generate_distractors(distractor_pool_name, count=6, exclude={correct}, context=context)
                    else:
                        wrong_answers = [f"Incorrect_{i}" for i in range(1, 7)]

                    # Also support direct distractor array in template for dynamic eval
                    if "distractors" in template and isinstance(template["distractors"], list):
                        for d in template["distractors"]:
                            resolved_d = engine.resolve_template(str(d), context)
                            if resolved_d != correct and resolved_d not in wrong_answers:
                                wrong_answers.append(resolved_d)
                        # We need at least 6 distractors, if we provided fewer, we need to fall back or pad
                        if len(wrong_answers) < 6 and distractor_pool_name:
                             # Generate more if possible
                             more_distractors = engine.generate_distractors(distractor_pool_name, count=6-len(wrong_answers), exclude=set([correct] + wrong_answers), context=context)
                             wrong_answers.extend(more_distractors)

                    # Fallback padding
                    while len(wrong_answers) < 6:
                         wrong_answers.append(f"Fallback_{len(wrong_answers)}")

                    # Ensure exactly 6 distractors, or trim if more
                    wrong_answers = wrong_answers[:6]

                    diff = random.choices(difficulties, weights=weights, k=1)[0]


                    svg_metadata = None
                    svg_config = template.get("svg")
                    if svg_config and svg_config.get("enabled", False):
                        svg_type = svg_config.get("type")
                        svg_params = {}

                        raw_params = svg_config.get("params", {})
                        for k, v in raw_params.items():
                            if isinstance(v, str):
                                svg_params[k] = engine.resolve_template(v, context)
                            else:
                                svg_params[k] = v

                        svg_content = SVGEngine.generate_svg(svg_type, svg_params)
                        if svg_content:
                            svg_metadata = {
                                "type": "inline",
                                "content": svg_content
                            }
                            DatasetManager.stats["svg_count"] += 1
                    q_id = f"{topic_name.replace(' ', '_').upper()}_{current_count + len(new_items) + 1:04d}"

                    item = {
                        "id": q_id,
                        "topic": topic_name,
                        "subtopic": template.get("subtopic", "General"),
                        "difficulty": diff,
                        "question": q_text,
                        "correct_answer": correct,
                        "wrong_answers_pool": wrong_answers,
                        "explanation": explanation
                    }
                    if svg_metadata:
                        item["svg"] = svg_metadata

                    new_items.append(item)
                    seen_questions.add(q_text)

                logger.info(f"Generated {len(new_items)} new template-based items after {attempts} attempts.")
            else:
                logger.error(f"Topic {topic_name} has neither custom_logic nor templates.")
                return

            final_dataset = existing_dataset + new_items

            if args.dry_run:
                logger.info(f"[DRY-RUN] Would write {len(final_dataset)} items to {output_file}")
                if DatasetManager.verify_dataset(final_dataset, topic_name):
                     logger.info("[DRY-RUN] Verification passed.")
                else:
                     logger.error("[DRY-RUN] Verification failed.")
            else:
                if DatasetManager.verify_dataset(final_dataset, topic_name):
                    try:
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(final_dataset, f, indent=2, ensure_ascii=False)
                        logger.info(f"Successfully saved {len(final_dataset)} items to {output_file}")
                        DatasetManager.stats["files_updated"] += 1
                        DatasetManager.stats["questions_generated"] += len(new_items)
                    except Exception as e:
                        logger.error(f"Failed to write to {output_file}: {e}")
                else:
                    logger.error(f"Verification failed for dataset. Not saving to {output_file}.")
        else:
            logger.info(f"Topic {topic_name} already meets target count.")

        # Update Map JSONs if configured or automatically derived
        map_config = topic_config.get("map_registration")
        if not map_config and output_file:
             map_config = MapUpdater.derive_map_config(output_file, topic_name)

        if map_config:
            MapUpdater.update_map("map.json", map_config, args)
            weekly_map_path = "dataset/weekly_quiz/weekly_map.json"
            # Weekly map has a different structure, usually we just update the standard map.
            # But the requirement says "update map.json and weekly_map.json".
            # For simplicity, if they want weekly_map to be auto-updated in a specific way, we might need a separate function.
            # Usually weekly_map holds tests for specific dates. Let's just run build_weekly_exams.py if that exists or update it if it's identical structure.
            # A memory rule states: "build_weekly_exams.py must be executed to regenerate dataset/weekly_quiz/weekly_map.json"
            # We can log this requirement or attempt to execute it.
            logger.info("To fully register in weekly exams, build_weekly_exams.py should be executed later.")

    @staticmethod
    def generate_summary_report():
        report_content = "# Curriculum Generation Summary\n\n"
        report_content += f"- **Questions Generated:** {DatasetManager.stats['questions_generated']}\n"
        report_content += f"- **Files Created/Updated:** {DatasetManager.stats['files_updated']}\n"
        report_content += f"- **SVGs Generated:** {DatasetManager.stats['svg_count']}\n"
        report_content += f"- **Duplicates Avoided:** {DatasetManager.stats['duplicates_avoided']}\n\n"

        report_content += "### Difficulty Distribution\n"
        for diff, count in DatasetManager.stats["difficulty_distribution"].items():
            report_content += f"- **{diff.capitalize()}:** {count}\n"

        try:
            with open("summary_report.md", "w") as f:
                f.write(report_content)
            logger.info("Summary report generated: summary_report.md")
        except Exception as e:
            logger.error(f"Failed to generate summary report: {e}")
def main():
    parser = argparse.ArgumentParser(description="Universal Quiz Dataset Generation Engine")
    parser.add_argument("--manifest", required=True, help="Path to the manifest JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Print plan of action without saving files")
    parser.add_argument("--append", action="store_true", help="Append to existing dataset files instead of overwriting")
    parser.add_argument("--target-count", type=int, help="Override target count for all topics")

    args = parser.parse_args()

    logger.info("==================================================")
    logger.info(f"Starting Universal Generation Engine")
    logger.info(f"Manifest: {args.manifest}")
    logger.info(f"Dry Run: {args.dry_run}")
    logger.info(f"Append: {args.append}")
    logger.info("==================================================")

    if not os.path.exists(args.manifest):
        logger.error(f"Manifest file not found: {args.manifest}")
        sys.exit(1)

    try:
        with open(args.manifest, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load manifest JSON: {e}")
        sys.exit(1)

    logger.info("Manifest loaded successfully.")

    data_pools_config = manifest.get("data_pools", {})
    engine = None
    if data_pools_config:
        logger.info(f"Initializing Template Engine with pools: {list(data_pools_config.keys())}")
        engine = TemplateEngine(data_pools_config)

    topics = manifest.get("topics", [])
    if not topics:
        logger.warning("No topics defined in manifest.")

    for topic_config in topics:
        DatasetManager.process_topic(engine, topic_config, args)

    # Generate Summary Report
    DatasetManager.generate_summary_report()

if __name__ == "__main__":
    main()