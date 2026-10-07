from rag_engine import retrieve

TEST_QUESTIONS = [
 ('What is the minimum class attendance required?', ['80', 'attendance']),
 ('How much does it cost to replace a lost student identity card?', ['5000', 'identity']),
 ('How early should students arrive for summative assessment?', ['thirty', '30', 'minutes']),
 ('What is the late registration fee?', ['25,000', '25000', 'registration']),
]

passed = 0
for question, keywords in TEST_QUESTIONS:
    results = retrieve(question)
    combined = ' '.join(r['text'].lower() for r in results)
    ok = any(k.lower() in combined for k in keywords)
    print(('PASS' if ok else 'FAIL') + ': ' + question)
    print('Retrieved pages:', [r['page'] for r in results])
    passed += int(ok)
print(f'\nRetrieval test accuracy: {passed/len(TEST_QUESTIONS)*100:.1f}%')
