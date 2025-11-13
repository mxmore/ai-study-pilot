CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS vector;

-- Users table storing learners and instructors
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    full_name TEXT,
    role TEXT NOT NULL CHECK (role IN ('student', 'instructor', 'admin')),
    preferences JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Knowledge domains and granular knowledge points
CREATE TABLE IF NOT EXISTS knowledge_points (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT,
    prerequisites UUID[] DEFAULT ARRAY[]::UUID[],
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Question bank backed by embeddings for semantic retrieval
CREATE TABLE IF NOT EXISTS questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source TEXT NOT NULL,
    question_type TEXT NOT NULL CHECK (question_type IN ('single_choice', 'multiple_choice', 'true_false', 'short_answer', 'essay')),
    prompt TEXT NOT NULL,
    options JSONB,
    answer JSONB,
    solution TEXT,
    difficulty NUMERIC(3,2) DEFAULT 0.50,
    embedding VECTOR(1536),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_questions_embedding ON questions USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);

-- Link table between questions and knowledge points
CREATE TABLE IF NOT EXISTS question_knowledge (
    question_id UUID REFERENCES questions(id) ON DELETE CASCADE,
    knowledge_id UUID REFERENCES knowledge_points(id) ON DELETE CASCADE,
    weight NUMERIC(3,2) DEFAULT 1.0,
    PRIMARY KEY (question_id, knowledge_id)
);

-- Study plans and spaced repetition schedules
CREATE TABLE IF NOT EXISTS study_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE,
    cadence TEXT NOT NULL,
    settings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS plan_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID REFERENCES study_plans(id) ON DELETE CASCADE,
    knowledge_id UUID REFERENCES knowledge_points(id),
    due_at DATE NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'skipped')),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Session attempts capturing adaptive practice telemetry
CREATE TABLE IF NOT EXISTS question_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    question_id UUID REFERENCES questions(id) ON DELETE CASCADE,
    plan_item_id UUID REFERENCES plan_items(id),
    response JSONB,
    score NUMERIC(4,2),
    time_spent_seconds INT,
    feedback JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- AI generated study recommendations persisted per learner
CREATE TABLE IF NOT EXISTS recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    knowledge_focus UUID REFERENCES knowledge_points(id),
    summary TEXT NOT NULL,
    priority NUMERIC(3,2) DEFAULT 0.5,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Seed data
INSERT INTO users (email, hashed_password, full_name, role)
VALUES
('learner@example.com', '$2b$12$examplehashlearner', 'Alice Learner', 'student'),
('mentor@example.com', '$2b$12$examplehashmentor', 'Bob Mentor', 'instructor')
ON CONFLICT (email) DO NOTHING;

INSERT INTO knowledge_points (subject, code, title, description)
VALUES
('Mathematics', 'ALG-001', 'Linear Equations', 'Solve single variable linear equations'),
('Mathematics', 'ALG-002', 'Quadratic Functions', 'Analyze and solve quadratic functions'),
('Physics', 'PHY-101', 'Newtonian Mechanics', 'Understand laws of motion and forces')
ON CONFLICT (code) DO NOTHING;

INSERT INTO questions (source, question_type, prompt, options, answer, solution, difficulty, embedding)
VALUES
('manual_seed', 'single_choice', 'What is the solution to 2x + 3 = 11?',
 '[{"label": "A", "value": "2"}, {"label": "B", "value": "3"}, {"label": "C", "value": "4"}, {"label": "D", "value": "5"}]',
 '{"correct": ["C"]}',
 'Subtract 3 from both sides to get 2x = 8, then divide by 2 to find x = 4.',
 0.45,
 NULL),
('manual_seed', 'true_false', 'Newton\'s second law states that F = ma.', NULL,
 '{"correct": [true]}',
 'Force equals mass times acceleration.',
 0.30,
 NULL)
ON CONFLICT (id) DO NOTHING;

INSERT INTO question_knowledge (question_id, knowledge_id, weight)
SELECT q.id, kp.id, 1.0
FROM questions q
JOIN knowledge_points kp ON kp.code IN ('ALG-001', 'PHY-101')
WHERE q.prompt IN ('What is the solution to 2x + 3 = 11?', 'Newton''s second law states that F = ma.')
ON CONFLICT DO NOTHING;

INSERT INTO study_plans (user_id, title, description, start_date, cadence)
SELECT id, 'Algebra Foundations', '30 day bootcamp on algebra essentials', CURRENT_DATE, 'daily'
FROM users WHERE email = 'learner@example.com'
ON CONFLICT DO NOTHING;
