projects=(
  medtext-commons
  medtext-conv
  medtext-deid
  medtext-neg
  medtext-ner
  medtext-parse
  medtext-secsplit
  medtext-preprocess
  medtext-ssplit
  medtext
)
currentdir=$(pwd)
outdir=$currentdir/dist
[ -d "$outdir" ] || mkdir "$outdir"
echo "$outdir"
for project in "${projects[@]}"
do
  echo "$project"
  (cd "$project" && python -m build -n -o "$outdir")
done