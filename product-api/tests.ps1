# Pruebas CRUD con curl.exe (Windows PowerShell)
# Requisito: servidor corriendo -> uvicorn main:app --reload
$u = "http://127.0.0.1:8000/api/v1/products/"
$h = "Content-Type: application/json"

Write-Host "`n1. POST crear (201)"
curl.exe -i -X POST $u -H $h -d "{\"sku\":\"A001\",\"name\":\"Mouse\",\"price\":150.5,\"stock\":20}"

Write-Host "`n1b. POST SKU repetido (409)"
curl.exe -i -X POST $u -H $h -d "{\"sku\":\"A001\",\"name\":\"Otro\",\"price\":10,\"stock\":1}"

Write-Host "`n1c. POST precio negativo (422)"
curl.exe -i -X POST $u -H $h -d "{\"sku\":\"B001\",\"name\":\"X\",\"price\":-5,\"stock\":1}"

Write-Host "`n2. GET listar con paginacion y filtro (200)"
curl.exe -i "${u}?skip=0&limit=5&name=mou"

Write-Host "`n3. GET por id (200)"
curl.exe -i "${u}1"

Write-Host "`n3b. GET id inexistente (404)"
curl.exe -i "${u}999"

Write-Host "`n4. PUT reemplazo completo (200)"
curl.exe -i -X PUT "${u}1" -H $h -d "{\"sku\":\"A001\",\"name\":\"Mouse Gamer\",\"price\":299,\"stock\":15}"

Write-Host "`n5. PATCH actualizacion parcial (200)"
curl.exe -i -X PATCH "${u}1" -H $h -d "{\"price\":250,\"stock\":8}"

Write-Host "`n6. DELETE (204)"
curl.exe -i -X DELETE "${u}1"

Write-Host "`n6b. GET tras borrar (404)"
curl.exe -i "${u}1"
