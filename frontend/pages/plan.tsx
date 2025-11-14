import { useState } from 'react';
import { Layout } from '../components/Layout';

interface PlanItem {
  knowledgeCode: string;
  dueAt: string;
  status: 'pending' | 'completed' | 'skipped';
}

const initialPlan: PlanItem[] = [
  { knowledgeCode: 'ALG-001', dueAt: '2024-03-01', status: 'completed' },
  { knowledgeCode: 'ALG-002', dueAt: '2024-03-02', status: 'pending' },
  { knowledgeCode: 'PHY-101', dueAt: '2024-03-03', status: 'pending' }
];

export default function PlanPage() {
  const [plan] = useState(initialPlan);

  return (
    <Layout title="学习计划" subtitle="SRS打卡与长期记忆巩固">
      <section className="card">
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={{ textAlign: 'left' }}>知识点</th>
              <th style={{ textAlign: 'left' }}>复习日期</th>
              <th style={{ textAlign: 'left' }}>状态</th>
            </tr>
          </thead>
          <tbody>
            {plan.map(item => (
              <tr key={item.knowledgeCode}>
                <td>{item.knowledgeCode}</td>
                <td>{item.dueAt}</td>
                <td>{item.status === 'completed' ? '✅ 已完成' : '⏳ 待完成'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </Layout>
  );
}
