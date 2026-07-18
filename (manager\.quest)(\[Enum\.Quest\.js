(manager\.quest)(\[Enum\.Quest\.\w+\])( >= \d+)

($1$2$3 ||  $1$2< questChecker$2)

\n{0}(manager\.quest)(\[Enum\.Quest\.\w+\])( >= \d+)([^{]+)\{\n

($1$2$3 ||  $1$2< questChecker$2)$4
{
if ($1$2< questChecker$2){
manager.messFin = true
return}


if \(manager.quest\[Enum.Quest.\w+\]< questChecker\[Enum.Quest.\w+\]\)\{
manager.messFin = true
test.messEnter\(\{keyCode:13\}\)
return\}