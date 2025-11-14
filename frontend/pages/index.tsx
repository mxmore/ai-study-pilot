import Head from 'next/head';
import { Layout } from '../components/Layout';

const highlights = [
  {
    title: '个性化学习路径',
    description: '结合AI Agent和知识图谱动态规划学习旅程。'
  },
  {
    title: '自适应刷题',
    description: '根据实时掌握度推荐题目并即时评估。'
  },
  {
    title: '跨平台无缝体验',
    description: '移动端优先设计，兼容PC Web体验。'
  }
];

export default function HomePage() {
  return (
    <Layout title="AI考试学习助手" subtitle="用智能学习伙伴驱动长期进步">
      <Head>
        <title>AI Study Pilot</title>
      </Head>
      <section className="grid">
        {highlights.map(highlight => (
          <article key={highlight.title} className="card">
            <h2>{highlight.title}</h2>
            <p>{highlight.description}</p>
          </article>
        ))}
      </section>
    </Layout>
  );
}
