import sys
import os
import time

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from generate_accounting12 import AccountingKnowledgeBase, AdvancedAccountingQuestionEngine

def generate_acc_financial_statements():
    t0 = time.time()
    kb = AccountingKnowledgeBase(os.path.join(root_dir, "extracted_topics_accounting.json"))
    target = next(t for t in kb.get_topics() if "paper1_acc_financial_statements.json" in t["file"])
    output_dir = os.path.join(root_dir, "dataset/grade12/accounting")
    engine = AdvancedAccountingQuestionEngine(target)
    engine.build(output_dir)
    print(f"Finished generate_acc_financial_statements in {time.time() - t0:.2f}s")

if __name__ == "__main__":
    generate_acc_financial_statements()
