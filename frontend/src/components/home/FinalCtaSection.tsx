import Link from "next/link";
import styles from "./FinalCtaSection.module.css";

export function FinalCtaSection() {
  return (
    <section className={styles.section} aria-labelledby="final-cta-heading">
      <div className={styles.container}>
        <h2 id="final-cta-heading" className={styles.heading}>
          Comece seu primeiro Círculo hoje.
        </h2>
        <p className={styles.body}>
          Organize sua rede de apoio. Compartilhe responsabilidades.{" "}
          Cuide com mais tranquilidade.
        </p>
        <Link
          href="/login"
          className={styles.cta}
          aria-label="Criar meu Círculo gratuitamente"
        >
          Criar meu Círculo
        </Link>
      </div>
    </section>
  );
}
