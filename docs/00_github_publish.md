# GitHub에 저장소 게시

## 1. GitHub 저장소 생성

GitHub에서 새 public repository를 생성합니다.

```text
Repository name: dbx-gasentec-demo
Visibility: Public
Initialize with README: 해제
```

## 2. 로컬 폴더에서 최초 게시

PowerShell에서 저장소 루트로 이동한 후 실행합니다.

```powershell
git init
git branch -M main
git remote add origin https://github.com/<github-id>/dbx-gasentec-demo.git
git add .
git commit -m "Add GasEntec LNG Databricks demo"
git push -u origin main
```

`<github-id>`는 본인의 GitHub ID로 바꿉니다. 이미 remote가 있으면 다음으로 확인합니다.

```powershell
git remote -v
git status
git log --oneline -1
```

## 3. Databricks에서 Git folder 받기

1. Workspace에서 `Create` → `Git folder`를 선택합니다.
2. Repository URL에 GitHub 저장소 URL을 입력합니다.
3. Git provider로 GitHub를 선택합니다.
4. 생성된 Git folder에서 `README.md`를 엽니다.

모든 참가자가 개인 계정을 사용하므로 공용 사용자 접두사는 사용하지 않습니다. 각자 개인 Workspace 경로와 개인 GitHub 인증만 사용합니다.

## 4. 변경 사항 게시

```powershell
git status
git add .
git commit -m "Update GasEntec demo assets"
git push origin main
```

Databricks Git folder에서는 `Pull`로 최신 main 브랜치를 받습니다.
