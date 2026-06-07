/**
 * SkipLink — Accessibility-first navigation aid.
 *
 * Renders an anchor that is visually hidden until focused via keyboard,
 * then jumps focus directly to the main content area.
 * WCAG 2.2 SC 2.4.1: Bypass Blocks (Level A).
 */
export function SkipLink() {
  return (
    <a href="#main-content" className="skip-link">
      Pular para o conteúdo principal
    </a>
  );
}
