# ============================================================================
# Alfa-Broker API - PowerShell Test Script (Updated with Copropiedad fields)
# Run: .\test_api.ps1
# ============================================================================

$BaseUrl = "http://localhost:5000"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "    Alfa-Broker API - Test Suite" -ForegroundColor Cyan
Write-Host "    (With Copropiedad Fields)" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ----------------------------------------------------------------------------
# HEALTH CHECK TESTS
# ----------------------------------------------------------------------------
Write-Host "▶ HEALTH CHECK ENDPOINTS" -ForegroundColor Yellow
Write-Host ""

Write-Host "1. API Health Check" -ForegroundColor Green
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/health" -Method GET
    $response | ConvertTo-Json -Depth 5
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

Write-Host "2. Database Health Check" -ForegroundColor Green
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/health/db" -Method GET
    $response | ConvertTo-Json -Depth 5
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

Write-Host "3. Full System Health Check" -ForegroundColor Green
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/health/full" -Method GET
    $response | ConvertTo-Json -Depth 5
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

# ----------------------------------------------------------------------------
# ASEGURADORAS CRUD TESTS
# ----------------------------------------------------------------------------
Write-Host "▶ ASEGURADORAS CRUD OPERATIONS" -ForegroundColor Yellow
Write-Host ""

Write-Host "4. GET ALL - Listar todas las aseguradoras" -ForegroundColor Green
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/api/aseguradoras" -Method GET
    Write-Host "  Total: $($response.count) aseguradoras" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 5
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

Write-Host "5. GET BY ID - Obtener aseguradora ID=1" -ForegroundColor Green
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/api/aseguradoras/1" -Method GET
    $response | ConvertTo-Json -Depth 5
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

Write-Host "6. GET BY ID - Probar ID inexistente (404)" -ForegroundColor Green
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/api/aseguradoras/9999" -Method GET
    $response | ConvertTo-Json -Depth 5
} catch {
    Write-Host "Expected 404 Error" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "7. CREATE - Crear aseguradora COMPLETA con campos Copropiedad" -ForegroundColor Green
$createBody = @{
    nombre = "Seguros Test PowerShell"
    numeral_asistencia = "800-PS-TEST"
    correo_comercial = "test@powershell.com"
    correo_reclamaciones = "claims@powershell.com"
    direccion_oficina = "Calle PowerShell #123"
    contacto_asignado = "PowerShell User"
    respaldo_aseguradora = "Grupo PowerShell Testing"
    # Copropiedad - Asistencia
    cop_asistencia_area_comun = "vidrieria,plomeria,cerrajeria,electricista"
    cop_asistencia_area_privada = "vidrieria,plomeria,cerrajeria"
    # Copropiedad - Daños Materiales
    cop_dm_deducible_terremoto = "3,porcentaje,50000000"
    cop_dm_deducible_inundacion = "2,porcentaje,30000000"
    cop_dm_deducible_incendio = "10,porcentaje,20000000"
    cop_dm_deducible_amit = "10,porcentaje,15000000"
    cop_dm_deducible_tuberia_vidrio = "10,porcentaje,10000000"
    # Copropiedad - Daños Internos
    cop_di_deducible_maq_equipo = "10,porcentaje,5000000"
    cop_di_deducible_equipo_electronico = "10,porcentaje,5000000"
    # Copropiedad - Sustracción con Violencia
    cop_scv_deducible_maq_equipo = "10,porcentaje,3000000"
    cop_scv_deducible_equipo_electronico = "10,porcentaje,3000000"
    cop_scv_deducible_dineros = "10,porcentaje,1000000"
    cop_scv_deducible_muebles = "10,porcentaje,2000000"
    # Copropiedad - D&A
    cop_da_deducible_amparo_basico = "10,porcentaje,5000000"
    # Copropiedad - RCE Deducibles
    cop_rce_deducible_contratistas = "10,porcentaje,3000000"
    cop_rce_deducible_cruzada = "10,porcentaje,3000000"
    cop_rce_deducible_patronal = "10,porcentaje,3000000"
    cop_rce_deducible_parqueaderos = "10,porcentaje,2000000"
    cop_rce_deducible_gastos_medicos = "0,porcentaje,500000"
    # Copropiedad - RCE Sublimites
    cop_rce_sublimite_contratistas = "30,porcentaje_evento,null"
    cop_rce_sublimite_cruzada = "30,porcentaje_evento,null"
    cop_rce_sublimite_patronal = "30,porcentaje_evento,null"
    cop_rce_sublimite_parqueaderos = "20,porcentaje_evento,null"
    cop_rce_sublimite_gastos_medicos = "10,porcentaje_evento,null"
    # Copropiedad - Manejo
    cop_manejo_deducible_amparo_basico = "10,porcentaje,3000000"
    # Copropiedad - Transporte de Valores
    cop_tv_deducible_amparo_basico = "10,porcentaje,2000000"
} | ConvertTo-Json

$createdId = $null
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/api/aseguradoras" -Method POST -Body $createBody -ContentType "application/json"
    $response | ConvertTo-Json -Depth 5
    $createdId = $response.data.id
    Write-Host "  → ID creado: $createdId" -ForegroundColor Cyan
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

Write-Host "8. CREATE - Error sin nombre (400)" -ForegroundColor Green
$errorBody = @{ correo_comercial = "test@test.com" } | ConvertTo-Json
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/api/aseguradoras" -Method POST -Body $errorBody -ContentType "application/json"
    $response | ConvertTo-Json -Depth 5
} catch {
    Write-Host "Expected 400 Error - nombre is required" -ForegroundColor Yellow
}
Write-Host ""

if ($createdId) {
    Write-Host "9. UPDATE - Actualizar campos Copropiedad (ID=$createdId)" -ForegroundColor Green
    $updateBody = @{
        nombre = "Seguros Test PowerShell - ACTUALIZADO"
        cop_asistencia_area_comun = "vidrieria,plomeria,cerrajeria,electricista,fumigacion"
        cop_dm_deducible_terremoto = "2.5,porcentaje,45000000"
        cop_rce_deducible_contratistas = "8,porcentaje,2500000"
    } | ConvertTo-Json

    try {
        $response = Invoke-RestMethod -Uri "$BaseUrl/api/aseguradoras/$createdId" -Method PUT -Body $updateBody -ContentType "application/json"
        $response | ConvertTo-Json -Depth 5
    } catch {
        Write-Host "Error: $_" -ForegroundColor Red
    }
    Write-Host ""

    Write-Host "10. GET BY ID - Verificar actualizacion (ID=$createdId)" -ForegroundColor Green
    try {
        $response = Invoke-RestMethod -Uri "$BaseUrl/api/aseguradoras/$createdId" -Method GET
        # Show specific copropiedad fields that were updated
        Write-Host "  Campos actualizados:" -ForegroundColor Cyan
        Write-Host "    nombre: $($response.data.nombre)" -ForegroundColor White
        Write-Host "    cop_asistencia_area_comun: $($response.data.cop_asistencia_area_comun)" -ForegroundColor White
        Write-Host "    cop_dm_deducible_terremoto: $($response.data.cop_dm_deducible_terremoto)" -ForegroundColor White
        Write-Host "    cop_rce_deducible_contratistas: $($response.data.cop_rce_deducible_contratistas)" -ForegroundColor White
    } catch {
        Write-Host "Error: $_" -ForegroundColor Red
    }
    Write-Host ""

    Write-Host "11. DELETE - Eliminar aseguradora de prueba (ID=$createdId)" -ForegroundColor Green
    try {
        $response = Invoke-RestMethod -Uri "$BaseUrl/api/aseguradoras/$createdId" -Method DELETE
        $response | ConvertTo-Json -Depth 5
    } catch {
        Write-Host "Error: $_" -ForegroundColor Red
    }
    Write-Host ""

    Write-Host "12. GET BY ID - Verificar eliminacion (404)" -ForegroundColor Green
    try {
        $response = Invoke-RestMethod -Uri "$BaseUrl/api/aseguradoras/$createdId" -Method GET
        $response | ConvertTo-Json -Depth 5
    } catch {
        Write-Host "Expected 404 Error - Record deleted" -ForegroundColor Yellow
    }
    Write-Host ""
}

Write-Host "13. UPDATE - Error ID inexistente (404)" -ForegroundColor Green
$updateErrorBody = @{ nombre = "No existe" } | ConvertTo-Json
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/api/aseguradoras/9999" -Method PUT -Body $updateErrorBody -ContentType "application/json"
    $response | ConvertTo-Json -Depth 5
} catch {
    Write-Host "Expected 404 Error" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "14. DELETE - Error ID inexistente (404)" -ForegroundColor Green
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/api/aseguradoras/9999" -Method DELETE
    $response | ConvertTo-Json -Depth 5
} catch {
    Write-Host "Expected 404 Error" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "    ✓ Test Suite Completed" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
