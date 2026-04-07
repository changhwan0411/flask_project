``` mermaid
    %% 반드시 이렇게 시작해야 합니다
    erDiagram
    USER ||--o{ POST : "작성함"
    USER ||--o{ CHAT_MESSAGE : "전송함"
    POST ||--o{ CHAT_MESSAGE : "메시지함"

    USER {
        int id PK "사용자 고유 번호"
        string username "아이디"
        string password "비밀번호"
    }

    POST {
        int id PK "게시글 고유 번호"
        int author_id FK "작성자 ID (USER.id 참조)"
        string title "물건 제목"
        int price "가격"
    }
```