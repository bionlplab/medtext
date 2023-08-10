find . -type d -name ".pytest_cache" -exec rm -r "{}" \;
find . -type d -name "htmlcov" -exec rm -r "{}" \;
find . -type f -name ".coverage" -exec rm -r "{}" \;
find . -type d -name "*.egg-info" -exec rm -r "{}" \;
find . -type d -name "dist" -exec rm -r "{}" \;