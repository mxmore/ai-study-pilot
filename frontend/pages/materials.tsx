import { Layout } from '../components/Layout';

const documents = [
  {
    title: 'Linear Equations Guide',
    summary: '分步骤掌握一次方程求解技巧。',
    knowledgeCodes: ['ALG-001']
  },
  {
    title: 'Newtonian Mechanics Overview',
    summary: '理解牛顿三大定律与实践案例。',
    knowledgeCodes: ['PHY-101']
  }
];

export default function MaterialsPage() {
  return (
    <Layout title="资料阅读" subtitle="多模态资料助力理解">
      <section className="grid">
        {documents.map(doc => (
          <article key={doc.title} className="card">
            <h2>{doc.title}</h2>
            <p>{doc.summary}</p>
            <small>关联知识点：{doc.knowledgeCodes.join(', ')}</small>
          </article>
        ))}
      </section>
    </Layout>
  );
}
