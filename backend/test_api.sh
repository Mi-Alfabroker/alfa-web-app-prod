#!/bin/bash
# ============================================================================
# Alfa-Broker API - Test Script (Updated with Copropiedad fields)
# Run: chmod +x test_api.sh && ./test_api.sh
# ============================================================================

BASE_URL="http://localhost:5000"
CREATED_ID=""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}    Alfa-Broker API - Test Suite${NC}"
echo -e "${BLUE}    (With Copropiedad Fields)${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# ----------------------------------------------------------------------------
# HEALTH CHECK TESTS
# ----------------------------------------------------------------------------
echo -e "${YELLOW}▶ HEALTH CHECK ENDPOINTS${NC}"
echo ""

echo -e "${GREEN}1. API Health Check${NC}"
curl -s -X GET "${BASE_URL}/health" | python -m json.tool 2>/dev/null || curl -s -X GET "${BASE_URL}/health"
echo -e "\n"

echo -e "${GREEN}2. Database Health Check${NC}"
curl -s -X GET "${BASE_URL}/health/db" | python -m json.tool 2>/dev/null || curl -s -X GET "${BASE_URL}/health/db"
echo -e "\n"

echo -e "${GREEN}3. Full System Health Check${NC}"
curl -s -X GET "${BASE_URL}/health/full" | python -m json.tool 2>/dev/null || curl -s -X GET "${BASE_URL}/health/full"
echo -e "\n"

# ----------------------------------------------------------------------------
# ASEGURADORAS CRUD TESTS
# ----------------------------------------------------------------------------
echo -e "${YELLOW}▶ ASEGURADORAS CRUD OPERATIONS${NC}"
echo ""

echo -e "${GREEN}4. GET ALL - Listar todas las aseguradoras${NC}"
curl -s -X GET "${BASE_URL}/api/aseguradoras" | python -m json.tool 2>/dev/null || curl -s -X GET "${BASE_URL}/api/aseguradoras"
echo -e "\n"

echo -e "${GREEN}5. GET BY ID - Obtener aseguradora ID=1${NC}"
curl -s -X GET "${BASE_URL}/api/aseguradoras/1" | python -m json.tool 2>/dev/null || curl -s -X GET "${BASE_URL}/api/aseguradoras/1"
echo -e "\n"

echo -e "${GREEN}6. GET BY ID - Probar ID inexistente (404)${NC}"
curl -s -X GET "${BASE_URL}/api/aseguradoras/9999" | python -m json.tool 2>/dev/null || curl -s -X GET "${BASE_URL}/api/aseguradoras/9999"
echo -e "\n"

echo -e "${GREEN}7. CREATE - Crear aseguradora COMPLETA con campos Copropiedad${NC}"
RESPONSE=$(curl -s -X POST "${BASE_URL}/api/aseguradoras" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Seguros Test Script",
    "numeral_asistencia": "800-SCRIPT-01",
    "correo_comercial": "test@script.com",
    "correo_reclamaciones": "claims@script.com",
    "direccion_oficina": "Calle Script #123",
    "contacto_asignado": "Script User",
    "respaldo_aseguradora": "Grupo Script Testing",
    "cop_asistencia_area_comun": "vidrieria,plomeria,cerrajeria,electricista",
    "cop_asistencia_area_privada": "vidrieria,plomeria,cerrajeria",
    "cop_dm_deducible_terremoto": "3,porcentaje,50000000",
    "cop_dm_deducible_inundacion": "2,porcentaje,30000000",
    "cop_dm_deducible_incendio": "10,porcentaje,20000000",
    "cop_dm_deducible_amit": "10,porcentaje,15000000",
    "cop_dm_deducible_tuberia_vidrio": "10,porcentaje,10000000",
    "cop_di_deducible_maq_equipo": "10,porcentaje,5000000",
    "cop_di_deducible_equipo_electronico": "10,porcentaje,5000000",
    "cop_scv_deducible_maq_equipo": "10,porcentaje,3000000",
    "cop_scv_deducible_equipo_electronico": "10,porcentaje,3000000",
    "cop_scv_deducible_dineros": "10,porcentaje,1000000",
    "cop_scv_deducible_muebles": "10,porcentaje,2000000",
    "cop_da_deducible_amparo_basico": "10,porcentaje,5000000",
    "cop_rce_deducible_contratistas": "10,porcentaje,3000000",
    "cop_rce_deducible_cruzada": "10,porcentaje,3000000",
    "cop_rce_deducible_patronal": "10,porcentaje,3000000",
    "cop_rce_deducible_parqueaderos": "10,porcentaje,2000000",
    "cop_rce_deducible_gastos_medicos": "0,porcentaje,500000",
    "cop_rce_sublimite_contratistas": "30,porcentaje_evento,null",
    "cop_rce_sublimite_cruzada": "30,porcentaje_evento,null",
    "cop_rce_sublimite_patronal": "30,porcentaje_evento,null",
    "cop_rce_sublimite_parqueaderos": "20,porcentaje_evento,null",
    "cop_rce_sublimite_gastos_medicos": "10,porcentaje_evento,null",
    "cop_manejo_deducible_amparo_basico": "10,porcentaje,3000000",
    "cop_tv_deducible_amparo_basico": "10,porcentaje,2000000"
  }')
echo "$RESPONSE" | python -m json.tool 2>/dev/null || echo "$RESPONSE"
# Extract created ID for later tests
CREATED_ID=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin).get('data', {}).get('id', ''))" 2>/dev/null)
echo -e "${BLUE}  → ID creado: ${CREATED_ID}${NC}"
echo -e "\n"

echo -e "${GREEN}8. CREATE - Error sin nombre (400)${NC}"
curl -s -X POST "${BASE_URL}/api/aseguradoras" \
  -H "Content-Type: application/json" \
  -d '{"correo_comercial": "test@test.com"}' | python -m json.tool 2>/dev/null || \
curl -s -X POST "${BASE_URL}/api/aseguradoras" \
  -H "Content-Type: application/json" \
  -d '{"correo_comercial": "test@test.com"}'
echo -e "\n"

if [ -n "$CREATED_ID" ]; then
  echo -e "${GREEN}9. UPDATE - Actualizar campos Copropiedad (ID=${CREATED_ID})${NC}"
  curl -s -X PUT "${BASE_URL}/api/aseguradoras/${CREATED_ID}" \
    -H "Content-Type: application/json" \
    -d '{
      "nombre": "Seguros Test Script - ACTUALIZADO",
      "cop_asistencia_area_comun": "vidrieria,plomeria,cerrajeria,electricista,fumigacion",
      "cop_dm_deducible_terremoto": "2.5,porcentaje,45000000",
      "cop_rce_deducible_contratistas": "8,porcentaje,2500000"
    }' | python -m json.tool 2>/dev/null || \
  curl -s -X PUT "${BASE_URL}/api/aseguradoras/${CREATED_ID}" \
    -H "Content-Type: application/json" \
    -d '{
      "nombre": "Seguros Test Script - ACTUALIZADO",
      "cop_asistencia_area_comun": "vidrieria,plomeria,cerrajeria,electricista,fumigacion",
      "cop_dm_deducible_terremoto": "2.5,porcentaje,45000000",
      "cop_rce_deducible_contratistas": "8,porcentaje,2500000"
    }'
  echo -e "\n"

  echo -e "${GREEN}10. GET BY ID - Verificar actualización (ID=${CREATED_ID})${NC}"
  curl -s -X GET "${BASE_URL}/api/aseguradoras/${CREATED_ID}" | python -m json.tool 2>/dev/null || curl -s -X GET "${BASE_URL}/api/aseguradoras/${CREATED_ID}"
  echo -e "\n"

  echo -e "${GREEN}11. DELETE - Eliminar aseguradora de prueba (ID=${CREATED_ID})${NC}"
  curl -s -X DELETE "${BASE_URL}/api/aseguradoras/${CREATED_ID}" | python -m json.tool 2>/dev/null || curl -s -X DELETE "${BASE_URL}/api/aseguradoras/${CREATED_ID}"
  echo -e "\n"

  echo -e "${GREEN}12. GET BY ID - Verificar eliminación (404)${NC}"
  curl -s -X GET "${BASE_URL}/api/aseguradoras/${CREATED_ID}" | python -m json.tool 2>/dev/null || curl -s -X GET "${BASE_URL}/api/aseguradoras/${CREATED_ID}"
  echo -e "\n"
fi

echo -e "${GREEN}13. UPDATE - Error ID inexistente (404)${NC}"
curl -s -X PUT "${BASE_URL}/api/aseguradoras/9999" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "No existe"}' | python -m json.tool 2>/dev/null || \
curl -s -X PUT "${BASE_URL}/api/aseguradoras/9999" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "No existe"}'
echo -e "\n"

echo -e "${GREEN}14. DELETE - Error ID inexistente (404)${NC}"
curl -s -X DELETE "${BASE_URL}/api/aseguradoras/9999" | python -m json.tool 2>/dev/null || curl -s -X DELETE "${BASE_URL}/api/aseguradoras/9999"
echo -e "\n"

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}    ✓ Test Suite Completed${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""
echo -e "${YELLOW}Estructura de campos Copropiedad:${NC}"
echo -e "  Deducibles: porcentaje,tipo,minimo"
echo -e "  Ejemplo: 3,porcentaje,50000000 → 3% con mínimo de 50M"
echo -e ""
echo -e "  Sublímites: porcentaje,tipo_evento,valor"
echo -e "  Ejemplo: 30,porcentaje_evento,null → 30% del evento"
