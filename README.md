# slmethod

Statistical Learning Method 统计学习方法

## 代码规范

参考：<https://docs.python.org/3/tutorial>

### .vscode/settings.json

```json
{
  "python.pythonPath": "/Users/iosdevlog/.Envs/slmethod/bin/python",
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "yapf",
  "python.linting.flake8Args": ["--max-line-length=248"],
  "python.linting.pylintEnabled": false
}
```

- 字符串使用双引号： **""**

## 安装

```sh
pip install slmethod
```

## 开发

### 本地开发

```sh
pip3 install -e .
```

### 发布

```sh
python3 setup.py sdist bdist_wheel
twine upload dist/*
```

## License

slmethod is released under the MIT license. See [LICENSE](LICENSE) for details.
