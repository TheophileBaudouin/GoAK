# Pattern — Dashboard

## When to use

For the app's landing/home view: a glanceable overview of the user's data (counts, trends,
recent activity) with clear entry points to deeper screens. Not for data-entry screens.

## How to organize the information

1. **Top row**: key metrics as stat cards (KPI number + label + trend). 3–6 cards max.
2. **Second row**: the chart or table that explains the numbers (usage over time, breakdown).
3. **Side/third zone**: recent activity or quick actions.
4. Every card/chart is a **link/action into the underlying screen** — a dashboard that
   can't navigate is a dead end.
5. Empty state first: if there is no data, show `Empty` with the primary action instead of
   a wall of zeroes.

## Common mistakes

- 12 identical-looking cards (no hierarchy, nothing readable).
- Charts without labels/legends (see `ui-rules/05-accessibility.md`, color + label).
- Numbers with no context (no period, no comparison).
- Real-time polling for data that changes rarely — stale-but-labeled beats churn.

## Best practices

- One **primary** metric emphasized (larger card or first position); the rest secondary.
- Use `tabular-nums` for all numbers (`ui-rules/03-typography.md`).
- Charts: prefer the harvested `ui-sdk/components/evilcharts/` (echarts-line/bar/pie) or
  the base `Chart`; keep 1 chart type per dashboard for consistency.
- Respect spacing rules (8px/20px) and dark mode (tokens only).

## Components/blocks recommended

- `ui-sdk/blocks/blocks-so/stats-12.tsx` (usage dashboard stats) and `stats-01`–`stats-15`
  variants from the same registry (add more via the shadcn CLI if needed).
- `ui-sdk/components/evilcharts/charts/echarts-line-chart.tsx`, `echarts-bar-chart.tsx`,
  `echarts-composed-chart.tsx`.
- Frozen base: `Card`, `Table`, `Chart`, `Empty`, `Skeleton` (loading state).
