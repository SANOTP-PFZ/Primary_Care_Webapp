with open('DSS_Webapp.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all st.rerun() with safe_rerun()
content = content.replace('st.rerun()', 'safe_rerun()')

with open('DSS_Webapp.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done - replaced st.rerun() with safe_rerun()')
