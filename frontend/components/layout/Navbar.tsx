"use client";

import React from "react";
import Link from "next/link";
import styles from "../../styles/components/layout/Navbar.module.css";

export const Navbar = () => {
    return (
        <nav className={styles.navbar}>
            <div className={styles.container}>
                <div className={styles.brand}>
                    <img src="/logo.png" alt="Zenva Logo" style={{ width: '32px', height: '32px', borderRadius: '0.5rem' }} />
                    <span className={styles.brandText}>Zenva</span>
                </div>

                <div className={styles.navLinks}>
                    <Link href="/" className={styles.navLink}>Home</Link>
                    <Link href="/features" className={styles.navLink}>Features</Link>
                    <Link href="/how-it-works" className={styles.navLink}>How it works</Link>
                    <Link href="/practice" className={styles.navLink}>Practice</Link>
                </div>

                <div className={styles.actions}>
                    <Link href="/practice" className={styles.actionBtn}>
                        Start Free
                    </Link>
                </div>
            </div>
        </nav>
    );
};
