# hands_on_exp

実験・ハンズオン用のサンドボックスリポジトリ。

## mt_docs — マルチテナント文書管理（認可実験）

```
mt_docs/
  roles.py              # Role, Action, ROLE_PERMISSIONS
  models.py             # User, Organization, Membership, Document
  can.py                # can() 認可判定
  document_service.py   # 文書 CRUD + 認可
  experiment_authz.py   # Step 2 実験
  experiment_documents.py  # Step 3 実験
```

### 実行

```bash
cd hands_on_exp
python3 -m mt_docs.experiment_authz
python3 -m mt_docs.experiment_documents
```
