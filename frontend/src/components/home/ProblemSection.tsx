import styles from "./ProblemSection.module.css";

const PROBLEMS = [
  {
    title: "Sobrecarga",
    body: "Uma única pessoa lembra de tudo.",
  },
  {
    title: "Informações espalhadas",
    body: "Mensagens. Papéis. Ligações. Anotações. Nada está realmente organizado.",
  },
  {
    title: "Insegurança",
    body: "Quem ficou responsável? O medicamento já foi administrado? Alguém confirmou a consulta?",
  },
] as const;

export function ProblemSection() {
  return (
    <section id="problema" className={styles.section} aria-labelledby="problem-heading">
      <div className={styles.container}>
        <h2 id="problem-heading" className={styles.heading}>
          Quando tudo depende de uma pessoa, o cuidado fica mais difícil.
        </h2>
        <ul className={styles.cardList} role="list">
          {PROBLEMS.map((problem) => (
            <li key={problem.title} className={styles.cardItem}>
              <article className={styles.card}>
                <h3 className={styles.cardTitle}>{problem.title}</h3>
                <p className={styles.cardBody}>{problem.body}</p>
              </article>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
