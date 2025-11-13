import { useQuery } from '@tanstack/react-query';
import { Layout } from '../components/Layout';
import { getQuestions } from '../lib/api';

export default function PracticePage() {
  const { data, isLoading, error } = useQuery({ queryKey: ['questions'], queryFn: getQuestions });

  return (
    <Layout title="自适应刷题" subtitle="围绕知识点持续精进">
      <section className="card">
        {isLoading && <p>载入题目中...</p>}
        {error && <p>无法加载题目，请稍后再试。</p>}
        {data && (
          <ul>
            {data.map(question => (
              <li key={question.id} style={{ marginBottom: '1rem' }}>
                <strong>{question.prompt}</strong>
                {question.options && (
                  <ol>
                    {question.options.map(option => (
                      <li key={option.value}>{`${option.label}. ${option.value}`}</li>
                    ))}
                  </ol>
                )}
              </li>
            ))}
          </ul>
        )}
      </section>
    </Layout>
  );
}
