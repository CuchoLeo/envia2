# 📋 Próximos Pasos: Configuración de Emails de Contacto

**Fecha**: 9 de Diciembre de 2024
**Versión**: 1.3.3
**Estado**: ✅ Sistema listo, pendiente configuración de emails

---

## ✅ Lo que ya está listo

### 1. Sistema de Email Modificado
- ✅ `src/email_sender.py` actualizado para usar `email_contacto` de la base de datos
- ✅ Método `_get_cliente_email()` implementado
- ✅ Manejo de errores cuando no hay email configurado
- ✅ Registro de intentos fallidos en la base de datos

### 2. Herramientas Creadas
- ✅ `scripts/utils/actualizar_emails_clientes.py` - Utilidad para actualizar emails
  - Modo interactivo con menú
  - Actualización individual por CLI
  - Actualización masiva desde CSV
  - Listado de clientes con/sin email

- ✅ `data/emails_clientes_template.csv` - Plantilla con los 78 clientes
  - 40 requieren OC (alta prioridad)
  - 38 NO requieren OC (baja prioridad)
  - Formato listo para editar y cargar

### 3. Documentación Completa
- ✅ `docs/CAMBIO_EMAIL_CONTACTO.md` - Documentación técnica del cambio
- ✅ `docs/GUIA_ACTUALIZACION_EMAILS.md` - Guía paso a paso de uso
- ✅ `CHANGELOG.md` actualizado a v1.3.3

---

## 📊 Estado Actual de la Base de Datos

```
Total de clientes: 78
  ├─ Requieren OC: 40 (ALTA PRIORIDAD) 🔴
  └─ NO requieren OC: 38 (BAJA PRIORIDAD) 🟡

Clientes CON email configurado: 1/78 (1.3%)
  └─ WALVIS S.A. → victor.rodriguez@outlook.com

Clientes SIN email configurado: 77/78 (98.7%)
```

---

## 🎯 Siguiente Paso CRÍTICO

### Opción A: Actualización Masiva (Recomendado)

**1. Editar plantilla CSV**
```bash
# Abrir en tu editor preferido
open data/emails_clientes_template.csv
```

**2. Reemplazar emails de placeholder por emails reales**

Enfócate primero en los **40 clientes que REQUIEREN OC** (sección superior del CSV):

```csv
# Antes:
SAVAL,contacto@saval.com
SPARTA,contacto@sparta.com

# Después (con emails reales):
SAVAL,compras@saval.cl
SPARTA,adquisiciones@sparta.cl
```

**3. Cargar los emails**
```bash
python scripts/utils/actualizar_emails_clientes.py \
  --archivo data/emails_clientes_template.csv
```

**4. Verificar**
```bash
python scripts/utils/actualizar_emails_clientes.py --todos
```

---

### Opción B: Actualización Individual (Para testing)

Actualizar algunos clientes de prueba:

```bash
# Ejemplo: actualizar 3 clientes
python scripts/utils/actualizar_emails_clientes.py --cliente "SAVAL" --email "compras@saval.cl"
python scripts/utils/actualizar_emails_clientes.py --cliente "SPARTA" --email "adquisiciones@sparta.cl"
python scripts/utils/actualizar_emails_clientes.py --cliente "SOPROLE S.A." --email "oc@soprole.cl"
```

---

## 🔥 Clientes PRIORITARIOS (Requieren OC)

Estos **40 clientes** necesitan email configurado URGENTEMENTE:

```
1. SAVAL
2. SPARTA
3. WALVIS S.A. ✅ (ya tiene email)
4. ISAMAY S.A.
5. TURISMOTOUR SPA
6. CAJA 18
7. CENTRAL DE COMPRAS MINEDUC
8. BIOBIO
9. COMSA
10. SOPROLE S.A.
11. KIA-INDUMOTORA
12. HYUNDAI
13. AUTOMOTORA DEL PACÍFICO
14. INDUMOTORA ONE
15. COSEMAR SERVICIOS INDUSTRIALES SPA
16. PRESERVA SPA
17. CEMARC
18. UNICON
19. UNACEM
20. PRODUCTOS FERNANDEZ S.A.
21. LABORATORIO ELEA
22. EVERLLENCE (EX MAN ENERGY SOLUTIONS)
23. COMERCIAL SANTA ELENA S.A.
24. SAN JOSE FARMS SPA
25. EXPORTADORA BAIKA S.A.
26. GESTACCION CONSULTOREES S.A.
27. LA CEIBA LTDA.
28. WILA SPA
29. BIOTEC
30. SISDEF
31. IST
32. COAGRA
33. BANAGRO S.A.
34. MORKEN
35. CLP INSUMOS
36. BCI SEGUROS GENERALES S.A.
37. EXELTIS CHILE SPA
38. SANTA ROSA CHILE ALIMENTOS LTDA.
39. TECNORED S.A.
40. MULTIACEROS S.A.
```

---

## 🧪 Probar el Sistema

### 1. Verificar emails configurados

```bash
python scripts/utils/ver_clientes_con_email.py
```

### 2. Probar con una reserva de prueba

Una vez que tengas al menos un cliente con email configurado (además de WALVIS S.A.):

```bash
# Generar PDF de prueba con ese cliente
python scripts/testing/generar_pdf_prueba.py

# O procesar un PDF real
# El sistema automáticamente:
# 1. Creará la reserva
# 2. Buscará el email del cliente
# 3. Enviará solicitud de OC
```

### 3. Monitorear logs

```bash
tail -f logs/sistema_$(date +%Y%m%d).log
```

Buscar líneas como:
```
INFO | EmailSender | Enviando correo a compras@saval.cl: Solicitud de Orden de Compra - Reserva ABC123
INFO | EmailSender | ✅ Correo enviado exitosamente a compras@saval.cl
```

O errores si falta email:
```
WARNING | EmailSender | No se encontró email de contacto para agencia: NUEVA EMPRESA
ERROR | EmailSender | No hay email de contacto configurado para NUEVA EMPRESA
```

---

## 📝 Plantilla para Solicitar Emails

Si necesitas solicitar los emails a otra persona/departamento:

```
Asunto: 🚨 URGENTE: Emails de contacto para sistema de OC

Hola [Nombre],

Para que el sistema de seguimiento de órdenes de compra funcione correctamente,
necesito los emails de contacto de los siguientes 40 clientes que REQUIEREN OC:

SAVAL
SPARTA
ISAMAY S.A.
TURISMOTOUR SPA
CAJA 18
...
[lista completa de 40 clientes]

Formato requerido (CSV):
NOMBRE_CLIENTE,email@dominio.com

Ejemplo:
SAVAL,compras@saval.cl
SPARTA,adquisiciones@sparta.cl

⏰ Prioridad: ALTA - Sin estos emails, el sistema no puede enviar solicitudes

Gracias!
```

---

## ⚠️ Recordatorios Importantes

### 1. Coincidencia Exacta de Nombres
El nombre en el CSV debe coincidir EXACTAMENTE con el de la BD:
- ✅ `SAVAL` (correcto)
- ❌ `saval` (mayúsculas diferentes)
- ❌ `Saval` (mayúsculas diferentes)

### 2. Sin Email = Sin Solicitudes
Si un cliente **requiere OC** pero **no tiene email**:
- ❌ El sistema NO enviará solicitudes
- ⚠️ Se registrará error en la BD
- 📝 Aparecerá en logs como "SIN EMAIL"

### 3. Validación de Emails
El sistema valida formato básico:
- Debe contener `@`
- Debe tener dominio con punto (`.`)

---

## 🔧 Comandos Útiles

### Ver estado general
```bash
cd scripts/database && python limpiar_base_datos.py --stats
```

### Listar clientes sin email
```bash
python scripts/utils/actualizar_emails_clientes.py --sin-email
```

### Ver todos los clientes con emails
```bash
python scripts/utils/actualizar_emails_clientes.py --todos
```

### Modo interactivo (menú)
```bash
python scripts/utils/actualizar_emails_clientes.py
```

---

## 📚 Documentación Relacionada

- `docs/GUIA_ACTUALIZACION_EMAILS.md` - Guía completa de uso
- `docs/CAMBIO_EMAIL_CONTACTO.md` - Documentación técnica
- `CHANGELOG.md` - Historial de cambios (v1.3.3)
- `data/emails_clientes_template.csv` - Plantilla editable

---

## ✅ Checklist

- [x] Sistema de email modificado
- [x] Scripts de actualización creados
- [x] Plantilla CSV generada
- [x] Documentación completa
- [ ] **PENDIENTE**: Obtener emails reales de los 40 clientes prioritarios
- [ ] **PENDIENTE**: Cargar emails en la base de datos
- [ ] **PENDIENTE**: Probar con reserva real
- [ ] **PENDIENTE**: Validar envío de correos

---

**Última actualización**: 9 de Diciembre de 2024, 14:20
**Responsable**: Sistema actualizado por Claude Code
**Contacto**: Ver documentación en `docs/`
