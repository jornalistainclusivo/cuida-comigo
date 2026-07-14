import styles from "./AccessibilitySection.module.css";

const FEATURES = [
  "Compatibilidade com leitores de tela",
  "Navegação por teclado",
  "Contraste conforme WCAG 2.2",
  "Tipografia escalável",
  "Interface simples e inclusiva",
] as const;

export function AccessibilitySection() {
  return (
    <section className={styles.section} aria-labelledby="accessibility-heading">
      <div className={styles.container}>
        <h2 id="accessibility-heading" className={styles.heading}>
          Feita para todas as pessoas.
        </h2>
        <p className={styles.body}>
          A Em Círculo foi desenvolvida seguindo princípios de acessibilidade desde a arquitetura do produto.
        </p>
        <ul className={styles.featureList} role="list">
          {FEATURES.map((feature) => (
            <li key={feature} className={styles.featureItem}>
              <span className={styles.featureMarker} aria-hidden="true">—</span>
              {feature}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
