# Security Checklist - AI Tools Framework

## 🔒 **Pre-Publication Security Checklist**

### ✅ **Environment Variables Protection**
- [ ] `.env` file is in `.gitignore`
- [ ] `.env.example` template is created (without real credentials)
- [ ] No API keys or passwords in any committed files
- [ ] No sensitive URLs or endpoints exposed
- [ ] All placeholder values are clearly marked

### ✅ **Git Security**
- [ ] Run `git status` to check staged files
- [ ] Review `git diff --cached` before committing
- [ ] Verify `.gitignore` is working: `git check-ignore .env`
- [ ] No sensitive files in git history

### ✅ **Code Security**
- [ ] No hardcoded API keys in Python files
- [ ] No email passwords in source code
- [ ] No database credentials in code
- [ ] All sensitive data uses environment variables

### ✅ **Documentation Security**
- [ ] README examples use placeholder values
- [ ] Documentation doesn't contain real API keys
- [ ] Configuration examples are sanitized
- [ ] No personal information in comments

## 🛡️ **Security Commands**

### Check for accidentally staged secrets:
```bash
# Check what's staged for commit
git diff --cached

# Check if .env is ignored
git check-ignore .env

# Search for potential secrets in staged files
git diff --cached | grep -i "key\|password\|token\|secret"
```

### Emergency: Remove accidentally committed secrets:
```bash
# If you accidentally commit secrets, immediately:
1. Change all exposed credentials
2. Remove from git history:
   git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch .env' --prune-empty --tag-name-filter cat -- --all
3. Force push: git push origin --force --all
```

## 🔍 **Regular Security Checks**

### Weekly:
- [ ] Rotate API keys
- [ ] Check for any new sensitive files
- [ ] Review git history for leaks

### Before Each Commit:
- [ ] `git status` - verify only intended files
- [ ] `git diff --cached` - review changes
- [ ] No secrets in commit message

### Before Publishing:
- [ ] Complete security audit
- [ ] Test with fresh `.env` from `.env.example`
- [ ] Verify all examples use placeholders

## 🚨 **Red Flags - Never Commit These**

### Files:
- `.env`, `.env.local`, etc.
- `secrets.json`, `config.ini` with credentials
- `database.db` with real data
- Log files with sensitive information

### Content:
- `SERPER_API_KEY=your-actual-api-key`
- `password="realpassword"`
- `smtp_user="real@email.com"`
- Personal email addresses
- Real webhook URLs
- Database connection strings

## 🔧 **Environment Setup Best Practices**

### Development:
1. Copy `.env.example` to `.env`
2. Fill in your development credentials
3. Never commit `.env`
4. Use test accounts when possible

### Production:
1. Use environment variables directly
2. Consider secrets management (Azure Key Vault, AWS Secrets, etc.)
3. Separate production and development credentials
4. Regular credential rotation

## 🛠️ **Tools for Security**

### Git Hooks (optional):
Create `.git/hooks/pre-commit`:
```bash
#!/bin/sh
# Pre-commit hook to check for secrets
if grep -r "SERPER_API_KEY.*sk-" --include="*.py" --include="*.json" .; then
    echo "ERROR: Found potential API key in commit!"
    exit 1
fi
```

### VS Code Extensions:
- GitLens - See file history and changes
- Git History - Track all modifications
- Password Protect - Highlight potential secrets

### Manual Verification:
```bash
# Search for potential secrets in your codebase
grep -r "api.key\|password\|secret" --include="*.py" .
```

---

## ⚠️ **If You Accidentally Commit Secrets**

### Immediate Actions:
1. **Rotate all exposed credentials immediately**
2. **Remove from git history** (see commands above)
3. **Notify relevant services** if applicable
4. **Update documentation** if credentials were public

### Prevention:
- Use this checklist every time
- Set up git hooks
- Regular security audits
- Team training on security practices

---

**Remember: Security is not a one-time setup, it's an ongoing practice!** 🔒
