import Link from "next/link";
import styles from "./HeroSection.module.css";

export function HeroSection() {
  return (
    <section className={styles.hero} aria-labelledby="hero-heading">
      <div className={styles.heroContent}>
        <h1 id="hero-heading" className={styles.headline}>
          Organize sua rede de apoio<br />
          <span className={styles.highlight}>em um único lugar.</span>
        </h1>
        <p className={styles.subtext}>
          A Em Círculo ajuda familiares, cuidadores e pessoas de apoio a compartilhar
          tarefas, medicamentos e informações, reduzindo a sobrecarga de quem coordena o cuidado.
        </p>
        <div className={styles.ctaGroup}>
          <Link
            href="/login"
            className={`btn btn--primary ${styles.ctaPrimarySize}`}
            aria-label="Criar meu Círculo gratuitamente"
          >
            Criar meu Círculo
          </Link>
          <a
            href="#como-funciona"
            className={styles.ctaSecondary}
            aria-label="Ir para a seção Como Funciona"
          >
            Conheça a plataforma
          </a>
        </div>
      </div>
    </section>
  );
}
