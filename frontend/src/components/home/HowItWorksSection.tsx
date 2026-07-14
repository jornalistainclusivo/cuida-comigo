import styles from "./HowItWorksSection.module.css";

const STEPS = [
  { step: 1, description: "Crie um Círculo." },
  { step: 2, description: "Convide familiares e pessoas de confiança." },
  { step: 3, description: "Compartilhem tarefas, medicamentos e informações." },
] as const;

export function HowItWorksSection() {
  return (
    <section
      id="como-funciona"
      className={styles.section}
      aria-labelledby="how-it-works-heading"
    >
      <div className={styles.container}>
        <h2 id="how-it-works-heading" className={styles.heading}>
          Começar leva apenas alguns minutos.
        </h2>
        <ol className={styles.stepList}>
          {STEPS.map(({ step, description }) => (
            <li key={step} className={styles.stepItem}>
              <span className={styles.stepNumber} aria-hidden="true">
                {step}
              </span>
              <h3 className={styles.stepDescription}>{description}</h3>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
