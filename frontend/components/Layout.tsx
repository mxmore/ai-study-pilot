import Link from 'next/link';
import { ReactNode } from 'react';

const links = [
  { href: '/', label: '首页' },
  { href: '/practice', label: '刷题' },
  { href: '/materials', label: '资料阅读' },
  { href: '/report', label: '学习报告' },
  { href: '/plan', label: '学习计划' }
];

interface LayoutProps {
  title: string;
  subtitle?: string;
  children: ReactNode;
}

export function Layout({ title, subtitle, children }: LayoutProps) {
  return (
    <>
      <nav className="navbar">
        <div>
          <strong>AI Study Pilot</strong>
        </div>
        <div className="nav-links">
          {links.map(link => (
            <Link key={link.href} href={link.href}>
              {link.label}
            </Link>
          ))}
        </div>
      </nav>
      <main>
        <header className="card">
          <h1>{title}</h1>
          {subtitle && <p>{subtitle}</p>}
        </header>
        {children}
      </main>
    </>
  );
}
