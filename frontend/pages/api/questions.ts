import type { NextApiRequest, NextApiResponse } from 'next';

const questions = [
  {
    id: 'q-1',
    prompt: 'What is the solution to 2x + 3 = 11?',
    question_type: 'single_choice',
    options: [
      { label: 'A', value: '2' },
      { label: 'B', value: '3' },
      { label: 'C', value: '4' },
      { label: 'D', value: '5' }
    ],
    difficulty: 0.45,
    knowledge_codes: ['ALG-001']
  },
  {
    id: 'q-2',
    prompt: "Newton's second law states that F = ma.",
    question_type: 'true_false',
    knowledge_codes: ['PHY-101']
  }
];

export default function handler(_req: NextApiRequest, res: NextApiResponse) {
  res.status(200).json(questions);
}
