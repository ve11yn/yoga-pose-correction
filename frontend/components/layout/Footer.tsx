"use client";

import React from "react";
import Link from "next/link";
import styles from "../../styles/components/layout/Footer.module.css";

export const Footer = () => {
    return (
        <footer className={styles.footer}>
            <div className={styles.container}>
                <div className={styles.grid}>
                    {/* Brand Column */}
                    <div className={styles.brandColumn}>
                        <div className={styles.brand}>
                            <img src="/logo.png" alt="Zenva Logo" style={{ width: '32px', height: '32px', borderRadius: '0.5rem' }} />
                            <span className={styles.brandText}>Zenva</span>
                        </div>
                        <p className={styles.description}>
                            Empowering your yoga journey with cutting-edge computer vision technology. Practice safer, smarter, and better.
                        </p>
                        <div className={styles.socialLinks}>
                            {['Twitter', 'Instagram', 'LinkedIn', 'Github'].map((social) => (
                                <a key={social} href="#" className={styles.socialIcon}>
                                    <span className="sr-only">{social}</span>
                                    <div className={styles.dot} />
                                </a>
                            ))}
                        </div>
                    </div>

                    {/* Links Columns */}
                    <div>
                        <h4 className={styles.columnTitle}>Product</h4>
                        <ul className={styles.linksList}>
                            <li><Link href="/features" className={styles.link}>Features</Link></li>
                            <li><Link href="/how-it-works" className={styles.link}>How it works</Link></li>
                            <li><Link href="/practice" className={styles.link}>Start Practice</Link></li>
                            <li><a href="#" className={styles.link}>Technology</a></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className={styles.columnTitle}>Company</h4>
                        <ul className={styles.linksList}>
                            <li><a href="#" className={styles.link}>About</a></li>
                            <li><a href="#" className={styles.link}>Blog</a></li>
                            <li><a href="#" className={styles.link}>Careers</a></li>
                            <li><a href="#" className={styles.link}>Contact</a></li>
                        </ul>
                    </div>

                    {/* Newsletter */}
                    <div className={styles.newsletterColumn}>
                        <h4 className={styles.columnTitle}>Stay Updated</h4>
                        <p className={styles.description} style={{ marginBottom: '1rem' }}>Get the latest yoga tips and AI updates.</p>
                        <div className={styles.inputGroup}>
                            <input
                                type="email"
                                placeholder="Enter your email"
                                className={styles.input}
                            />
                            <button className={styles.subscribeBtn}>
                                Subscribe
                            </button>
                        </div>
                    </div>
                </div>

                <div className={styles.bottomBar}>
                    <p>© 2024 Zenva. All rights reserved.</p>
                    <div className={styles.legalLinks}>
                        <a href="#" className={styles.link}>Privacy Policy</a>
                        <a href="#" className={styles.link}>Terms of Service</a>
                        <a href="#" className={styles.link}>Cookie Policy</a>
                    </div>
                </div>
            </div>
        </footer>
    );
};
