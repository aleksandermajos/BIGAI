from ENGINE.ALL.PYTHON_ENV_CHECK import check_packages

d = {
    'numpy': '1.21.2',
    'scipy': '1.7.0',
    'matplotlib': '3.4.3',
    'sklearn': '1.0',
    'pandas': '1.3.2',
    'torch': '1.8.0',
    'torchvision': '0.9.0'
}
check_packages(d)