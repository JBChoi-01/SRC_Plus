# 멤버 리뷰 페이지 설정 (최초 1회, 약 5분)

`member.html` 은 지금 **로컬 데모 모드**(내 브라우저에만 저장)로 동작합니다.
멤버들과 실시간 공유하려면 무료 Firebase(Firestore) 프로젝트를 연결하세요.

1. https://console.firebase.google.com → 프로젝트 추가 (Analytics 불필요)
2. 빌드 → **Firestore Database** → 데이터베이스 만들기 (프로덕션 모드, 리전 `asia-northeast3` 서울)
3. Firestore → **규칙** 탭에 `firestore.rules` 내용을 붙여넣고 게시
4. 프로젝트 설정 → 일반 → 내 앱 → **웹 앱(</>) 추가** → 표시되는 `firebaseConfig` 값 확인
5. `member.html` 안의 `FIREBASE_CONFIG` 에 `apiKey / authDomain / projectId / appId` 입력 후 커밋
6. 접속: `https://<사이트주소>/member.html` (링크 없이 주소만 공유, noindex)

## 사용법
- 왼쪽: 리포트 목록(초안 포함, 미해결 제안 수 배지) / 가운데: 리포트 / 오른쪽: 제안
- 본문의 문장을 드래그 → **＋ 이 부분에 제안** → 입력하면 즉시 저장되고 접속 중인 모두에게 실시간 반영
- 카드 클릭: 해당 문장 강조 + 답글, **해결됨** 처리, 본인 제안 삭제
- 새 리포트는 `build.py` 가 자동으로 목록에 반영 (GitHub Action이 `member.html` 도 갱신)

## 보안
apiKey 는 웹 앱 식별용이라 공개돼도 되지만, 규칙상 **주소를 아는 사람은 누구나 읽고 쓸 수 있습니다**(링크를 아는 사람만 접근하는 수준).
스팸/삭제가 걱정되면 Firebase Authentication(익명 로그인 + 공유 코드) 또는 Google 로그인 + 허용 이메일 목록으로 강화할 수 있습니다.
