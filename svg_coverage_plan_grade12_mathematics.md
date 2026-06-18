# SVG Coverage Plan: Grade 12 Mathematics

This document outlines the strategy for injecting SVG visual aids into the Grade 12 Mathematics curriculum datasets. It serves as a blueprint for implementing dynamic SVGs directly into the question generation scripts.

## Frontend Compatibility Notes (Global)
- All generated SVGs must be valid, inline HTML strings.
- SVGs will be injected into the generated JSON datasets under the property: `"svg": {"content": "<svg>...</svg>"}`.
- The frontend (`quiz.html`, `weekly_quiz.html`, `test_run_quiz.html`) expects this structure and will render it directly below the question text into a dedicated container (`#question-svg-container`).
- SVGs must use a `viewBox` for responsiveness and have appropriate styling (e.g., `width="100%"`, `max-width: 300px;`, `margin: auto; display: block;`).
- Avoid relying on external CSS classes; use inline stroke and fill colors to ensure rendering consistency in offline modes or Android WebViews.

---

## 1. Euclidean Geometry (Priority 1)
- **SVG Coverage:** 95-100%
- **SVG Types:** Intersecting lines, triangles, circles with chords/tangents, cyclic quadrilaterals.
- **Required Parameters:** `shape_type` (e.g., circle_tangent, cyclic_quad), `labels` (vertices like A, B, C), `angles` (to display text at specific nodes).
- **Question Categories Using It:** angle relationships, triangle theorems, cyclic quadrilaterals.
- **Example Generated SVG Concept:** A circle with an inscribed quadrilateral and one extended side forming an exterior angle.

## 2. Functions and Graphs (Priority 2)
- **SVG Coverage:** 70-80%
- **SVG Types:** Coordinate grid with function curves (linear, quadratic, cubic, hyperbolic, exponential).
- **Required Parameters:** `grid_bounds` (x_min, x_max, y_min, y_max), `functions` (list of formulas/points to plot), `asymptotes`, `key_points` (intercepts, turning points).
- **Question Categories Using It:** quadratic functions, cubic functions, transformations, intercepts and turning points.
- **Example Generated SVG Concept:** A Cartesian plane showing a parabola and a straight line intersecting.

## 3. Analytical Geometry (Priority 3)
- **SVG Coverage:** 80-100%
- **SVG Types:** Coordinate grid with plotted points, line segments, and basic polygons.
- **Required Parameters:** `points` (list of x,y coordinates with labels), `lines` (connecting specific points), `grid_lines` (boolean).
- **Question Categories Using It:** distance formula, midpoint formula, gradient of a line, equation of a line.
- **Example Generated SVG Concept:** Points A and B on a grid with a dashed line segment connecting them.

## 4. Trigonometry (Priority 4)
- **SVG Coverage:** 60-70%
- **SVG Types:** Right-angled triangles, non-right triangles, unit circle, trig graphs (sine/cosine waves), 3D planes.
- **Required Parameters:** `triangle_type`, `side_lengths`, `angles`, `wave_params` (amplitude, period, shift).
- **Question Categories Using It:** sine rule, cosine rule, solving trig equations (unit circle context), 2D/3D applications.
- **Example Generated SVG Concept:** A triangle with sides labeled 'a', 'b', and included angle '$\theta$'.

## 5. Statistics and Regression (Priority 5)
- **SVG Coverage:** 80-90%
- **SVG Types:** Scatter plots, lines of best fit, box-and-whisker plots, histograms, ogives.
- **Required Parameters:** `data_points` (for scatter), `quartiles` (min, Q1, median, Q3, max), `bins` (for histograms).
- **Question Categories Using It:** scatter plots, linear regression, standard deviation.
- **Example Generated SVG Concept:** A scatter plot with an overlaying regression line.

## 6. Differential Calculus (Priority 6)
- **SVG Coverage:** 60-70%
- **SVG Types:** Cubic graphs, tangent lines, area under the curve representations, geometric shapes for optimization.
- **Required Parameters:** `curve_type`, `tangent_point`, `shaded_regions`, `optimization_shape` (e.g., open box).
- **Question Categories Using It:** gradients of curves, turning points, optimization problems.
- **Example Generated SVG Concept:** A cubic curve showing local maximum and minimum turning points.

## 7. Probability (Priority 7)
- **SVG Coverage:** 40-50%
- **SVG Types:** Tree diagrams, Venn diagrams, two-way tables (rendered as SVG or HTML tables).
- **Required Parameters:** `nodes` (for tree), `probabilities` (edge weights), `sets` (for Venn overlaps).
- **Question Categories Using It:** tree diagrams, dependent events, basic probability.
- **Example Generated SVG Concept:** A two-branch tree diagram splitting into further branches.

## 8. Patterns and Sequences (Priority 8)
- **SVG Coverage:** 10-15%
- **SVG Types:** Dot patterns, block growth diagrams.
- **Required Parameters:** `pattern_type` (dots, blocks), `terms` (number of terms to visualize).
- **Question Categories Using It:** arithmetic sequences, geometric sequences.
- **Example Generated SVG Concept:** T1 = 1 block, T2 = 3 blocks, T3 = 6 blocks (visualizing triangular numbers).

## 9. Finance, Growth and Decay (Priority 9)
- **SVG Coverage:** 5-10%
- **SVG Types:** Investment timelines, exponential growth/depreciation curves.
- **Required Parameters:** `timeline_events` (T0, T1, T2 values), `curve_type`.
- **Question Categories Using It:** compound interest, depreciation.
- **Example Generated SVG Concept:** A horizontal timeline marking deposits and withdrawals over $n$ periods.

## 10. Algebra, Equations and Inequalities (Priority 10)
- **SVG Coverage:** 0-5%
- **SVG Types:** Number lines, interval notation diagrams, sign diagrams.
- **Required Parameters:** `roots` (critical values), `regions` (positive/negative indicators), `inclusion` (open/closed circles).
- **Question Categories Using It:** inequalities.
- **Example Generated SVG Concept:** A number line with critical values at -3 and 5, shaded between them with closed dots.
