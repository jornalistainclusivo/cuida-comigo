"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import Link from "next/link";
import Image from "next/image";
import styles from "./HomeHeader.module.css";

const NAV_LINKS = [
  { href: "#problema", label: "O Problema" },
  { href: "#solucao", label: "A Solução" },
  { href: "#como-funciona", label: "Como Funciona" },
] as const;

export function HomeHeader() {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);

  const closeMenu = useCallback(() => {
    setIsOpen(false);
    // Return focus to trigger button on close (WCAG 2.4.3)
    triggerRef.current?.focus();
  }, []);

  // Close on Escape key (WCAG 2.1.2)
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") closeMenu();
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, closeMenu]);

  // Focus first menu item when menu opens (WCAG 2.4.3)
  useEffect(() => {
    if (isOpen && menuRef.current) {
      const firstLink = menuRef.current.querySelector<HTMLAnchorElement>("a");
      firstLink?.focus();
    }
  }, [isOpen]);

  // Close on outside click
  useEffect(() => {
    if (!isOpen) return;

    const handleClick = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node) &&
          triggerRef.current && !triggerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, [isOpen]);

  return (
    <header className={styles.header} role="banner">
      <div className={styles.inner}>
        {/* Logo */}
        <Link
          href="/"
          className={styles.logo}
          aria-label="Em Círculo — página inicial"
        >
          <Image
            src="/logo.png"
            alt="Ícone Em Círculo"
            width={32}
            height={32}
            style={{ height: "32px", width: "auto" }}
          />
          <span>em círculo</span>
        </Link>

        {/* Desktop navigation */}
        <nav className={styles.desktopNav} aria-label="Menu Principal">
          <ul className={styles.navList} role="list">
            {NAV_LINKS.map(({ href, label }) => (
              <li key={href}>
                <a href={href} className={styles.navLink}>
                  {label}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        {/* Desktop CTA */}
        <div className={styles.desktopCta}>
          <Link href="/login" className={styles.btnOutline} aria-label="Entrar na plataforma">
            Entrar
          </Link>
        </div>

        {/* Hamburger button — mobile only */}
        <button
          ref={triggerRef}
          className={styles.hamburger}
          onClick={() => setIsOpen((prev) => !prev)}
          aria-expanded={isOpen}
          aria-controls="mobile-menu"
          aria-label={isOpen ? "Fechar menu" : "Abrir menu"}
          type="button"
        >
          {/* Animated icon: 3 bars → X */}
          <span className={`${styles.bar} ${isOpen ? styles.barTopOpen : ""}`} aria-hidden="true" />
          <span className={`${styles.bar} ${isOpen ? styles.barMidOpen : ""}`} aria-hidden="true" />
          <span className={`${styles.bar} ${isOpen ? styles.barBotOpen : ""}`} aria-hidden="true" />
        </button>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <nav
          id="mobile-menu"
          ref={menuRef}
          className={styles.mobileMenu}
          aria-label="Menu Mobile"
        >
          <ul className={styles.mobileNavList} role="list">
            {NAV_LINKS.map(({ href, label }) => (
              <li key={href}>
                <a
                  href={href}
                  className={styles.mobileNavLink}
                  onClick={closeMenu}
                >
                  {label}
                </a>
              </li>
            ))}
            <li className={styles.mobileCta}>
              <Link href="/login" className={styles.mobileCtaLink} onClick={closeMenu}>
                Entrar
              </Link>
            </li>
          </ul>
        </nav>
      )}
    </header>
  );
}
