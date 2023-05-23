## Build Container

docker build --rm -t ai_cos710 .

## Run Container

docker run --rm -v "$(pwd)/runs:/runs" -v "$(pwd)/data:/data" ai_cos710 -p 10 -r 1 -g 3 -i 75 -j 25 -s

## Grammer

<expr> := constant | parameter | <expr> <op> <expr>
<op> := + | - | / | \*
