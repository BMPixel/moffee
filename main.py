import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from markupsafe import Markup

def nl2br(value):
    return Markup(value.replace('\n', '<br>\n'))

# 设置 Jinja2 环境
template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'default')
env = Environment(loader=FileSystemLoader(template_dir))

# 添加自定义过滤器
env.filters['nl2br'] = nl2br

# 加载基础模板
template = env.get_template('base.html')

# 准备要填充到模板中的数据
data = {
    'title': 'My Awesome Presentation',
    'slides': [
        {
            'title': 'Welcome Slide',
            'content': 'Welcome to this awesome presentation!',
            'layout': 'top-down'
        },
        {
            'title': 'Key Points',
            'content': 'Here are the main takeaways:\n- Point 1\n- Point 2\n- Point 3',
            'layout': 'split'
        },
        {
            'title': 'Thank You',
            'content': 'Any questions?',
            'layout': 'top-down'
        }
    ]
}

# 渲染模板
output = template.render(data)

# 确保 tmp 目录存在
tmp_dir = os.path.join(os.path.dirname(__file__), 'tmp')
os.makedirs(tmp_dir, exist_ok=True)

# 将渲染后的 HTML 写入文件
output_file = os.path.join(tmp_dir, f'presentation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Presentation has been generated and saved to: {output_file}")