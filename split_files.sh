for file in ./raw_texts/*; do
  split -l 200 `echo "${file}"` `echo "${file}_"`
  rm `echo "${file}"`
done
