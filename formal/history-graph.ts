export type HistoryEdgeType = 'renamed' | 'split' | 'merged' | 'deprecated' | 'successor';

export type HistoryEdge = {
  from: string;
  to: string;
  type: HistoryEdgeType;
  evidenceId: string;
};

export function successors(entityId: string, edges: HistoryEdge[]): string[] {
  return edges
    .filter(edge => edge.from === entityId && ['split', 'merged', 'successor', 'renamed'].includes(edge.type))
    .map(edge => edge.to);
}

export function hasLineagePath(from: string, to: string, edges: HistoryEdge[]): boolean {
  const seen = new Set<string>();
  const queue = [from];
  while (queue.length) {
    const current = queue.shift()!;
    if (current === to) return true;
    if (seen.has(current)) continue;
    seen.add(current);
    queue.push(...successors(current, edges));
  }
  return false;
}
