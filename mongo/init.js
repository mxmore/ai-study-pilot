// MongoDB initialization script for content metadata and learner activity stream

const dbName = 'ai_study';
const db = db.getSiblingDB(dbName);

db.createCollection('documents');
db.createCollection('activity_logs');
db.createCollection('learning_snapshots');

db.documents.createIndex({ knowledgeCodes: 1, tags: 1 });
db.activity_logs.createIndex({ userId: 1, createdAt: -1 });
db.learning_snapshots.createIndex({ userId: 1, knowledgeCode: 1 }, { unique: true });

// Seed reference documents for the reading module
if (db.documents.countDocuments() === 0) {
  db.documents.insertMany([
    {
      title: 'Linear Equations Guide',
      sourceType: 'pdf',
      storageKey: 'documents/algebra/linear-equations.pdf',
      knowledgeCodes: ['ALG-001'],
      summary: 'Step-by-step strategies to solve single variable equations.',
      tags: ['algebra', 'fundamentals'],
      aiChunks: [],
      createdAt: new Date(),
    },
    {
      title: 'Newtonian Mechanics Overview',
      sourceType: 'web',
      storageKey: 'documents/physics/newtonian-mechanics.html',
      knowledgeCodes: ['PHY-101'],
      summary: 'Core concepts of Newton\'s laws with practical examples.',
      tags: ['physics', 'mechanics'],
      aiChunks: [],
      createdAt: new Date(),
    },
  ]);
}

// Seed adaptive learning snapshots per knowledge point
if (db.learning_snapshots.countDocuments() === 0) {
  const learnerId = '00000000-0000-0000-0000-000000000001';
  db.learning_snapshots.insertMany([
    {
      userId: learnerId,
      knowledgeCode: 'ALG-001',
      mastery: 0.35,
      lastReviewedAt: new Date(),
      nextReviewAt: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000),
      history: [],
    },
    {
      userId: learnerId,
      knowledgeCode: 'PHY-101',
      mastery: 0.20,
      lastReviewedAt: new Date(),
      nextReviewAt: new Date(Date.now() + 4 * 24 * 60 * 60 * 1000),
      history: [],
    },
  ]);
}

print('MongoDB initialization complete');
