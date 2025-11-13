import { Layout } from '../components/Layout';

const report = {
  mastery: [
    { knowledgeCode: 'ALG-001', score: 0.62 },
    { knowledgeCode: 'ALG-002', score: 0.41 },
    { knowledgeCode: 'PHY-101', score: 0.28 }
  ],
  streak: 5,
  recommendations: [
    '复习一次方程并尝试难度提升的练习。',
    '今日重点关注牛顿第二定律相关题目。'
  ]
};

export default function ReportPage() {
  return (
    <Layout title="学习报告" subtitle="掌握度评估与智能建议">
      <section className="card">
        <h2>知识点掌握度</h2>
        <ul>
          {report.mastery.map(item => (
            <li key={item.knowledgeCode}>
              {item.knowledgeCode}: {(item.score * 100).toFixed(0)}%
            </li>
          ))}
        </ul>
      </section>
      <section className="card">
        <h2>连续打卡</h2>
        <p>{report.streak} 天</p>
      </section>
      <section className="card">
        <h2>AI 建议</h2>
        <ul>
          {report.recommendations.map(text => (
            <li key={text}>{text}</li>
          ))}
        </ul>
      </section>
    </Layout>
  );
}
