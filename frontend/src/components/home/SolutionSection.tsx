import styles from "./SolutionSection.module.css";

const SOLUTIONS = [
  {
    title: "Compartilhe tarefas",
    body: "Todos sabem quem faz o quê.",
  },
  {
    title: "Medicamentos",
    body: "Registre administrações e evite esquecimentos ou doses duplicadas.",
  },
  {
    title: "Histórico",
    body: "Toda a rede acompanha as informações mais importantes.",
  },
  {
    title: "Convide pessoas",
    body: "Familiares, cuidadores e profissionais trabalham juntos.",
  },
  {
    title: "Avisos",
    body: "Centralize comunicados importantes e evite grupos confusos no WhatsApp.",
  },
  {
    title: "Arquivos",
    body: "Guarde receitas, exames e documentos médicos com segurança.",
  },
] as const;

export function SolutionSection() {
  return (
    <section
      id="solucao"
      className={styles.section}
      aria-labelledby="solution-heading"
    >
      <div className={styles.container}>
        <h2 id="solution-heading" className={styles.heading}>
          Um Círculo organiza tudo.
        </h2>
        <ul className={styles.cardList} role="list">
          {SOLUTIONS.map((solution) => (
            <li key={solution.title} className={styles.cardItem}>
              <article className={styles.card}>
                <h3 className={styles.cardTitle}>{solution.title}</h3>
                <p className={styles.cardBody}>{solution.body}</p>
              </article>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
