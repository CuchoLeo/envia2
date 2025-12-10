"""
Procesador de PDF para extraer información de reservas
Extrae datos estructurados del PDF de resumen de servicios
"""
import re
import json
from datetime import datetime
from typing import Dict, Optional, List, Any
from pathlib import Path
import pdfplumber
import PyPDF2
from loguru import logger


class PDFProcessor:
    """Procesa PDFs de resumen de servicios y extrae datos de reserva"""

    def __init__(self):
        self.logger = logger.bind(module="PDFProcessor")

    def extract_from_file(self, pdf_path: str) -> Optional[Dict[str, Any]]:
        """
        Extrae datos de un archivo PDF

        Args:
            pdf_path: Ruta al archivo PDF

        Returns:
            Diccionario con datos extraídos o None si falla
        """
        try:
            self.logger.info(f"Procesando PDF: {pdf_path}")

            # Intentar con pdfplumber primero (mejor para texto estructurado)
            try:
                return self._extract_with_pdfplumber(pdf_path)
            except Exception as e:
                self.logger.warning(f"pdfplumber falló, intentando con PyPDF2: {e}")
                return self._extract_with_pypdf2(pdf_path)

        except Exception as e:
            self.logger.error(f"Error procesando PDF {pdf_path}: {e}")
            return None

    def extract_from_bytes(self, pdf_bytes: bytes, filename: str = "documento.pdf") -> Optional[Dict[str, Any]]:
        """
        Extrae datos de bytes de PDF (útil para archivos adjuntos de correo)

        Args:
            pdf_bytes: Contenido del PDF en bytes
            filename: Nombre del archivo (para logging)

        Returns:
            Diccionario con datos extraídos o None si falla
        """
        try:
            self.logger.info(f"Procesando PDF desde bytes: {filename}")

            # Guardar temporalmente
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(pdf_bytes)
                tmp_path = tmp.name

            # Procesar
            result = self.extract_from_file(tmp_path)

            # Limpiar archivo temporal
            Path(tmp_path).unlink()

            return result

        except Exception as e:
            self.logger.error(f"Error procesando PDF desde bytes {filename}: {e}")
            return None

    def _extract_with_pdfplumber(self, pdf_path: str) -> Dict[str, Any]:
        """Extrae texto usando pdfplumber"""
        with pdfplumber.open(pdf_path) as pdf:
            # Extraer texto de todas las páginas
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"

            return self._parse_text(full_text)

    def _extract_with_pypdf2(self, pdf_path: str) -> Dict[str, Any]:
        """Extrae texto usando PyPDF2 (fallback)"""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            full_text = ""
            for page in pdf_reader.pages:
                full_text += page.extract_text() + "\n"

            return self._parse_text(full_text)

    def _parse_text(self, text: str) -> Dict[str, Any]:
        """
        Parsea el texto extraído y estructura los datos

        Args:
            text: Texto extraído del PDF

        Returns:
            Diccionario con datos estructurados
        """
        data = {}

        # Extraer ID de reserva
        id_match = re.search(r'ID:\s*(\d+)', text, re.IGNORECASE)
        if id_match:
            data['id_reserva'] = id_match.group(1)

        # Extraer LOC Interno
        loc_interno_match = re.search(r'LOC\s+Interno:\s*([A-Z0-9]+)', text, re.IGNORECASE)
        if loc_interno_match:
            data['loc_interno'] = loc_interno_match.group(1)
            # Si no hay ID, usar LOC Interno como id_reserva
            if 'id_reserva' not in data:
                data['id_reserva'] = loc_interno_match.group(1)

        # Extraer Localizador
        localizador_match = re.search(r'Localizador:\s*(\d+)', text, re.IGNORECASE)
        if localizador_match:
            data['localizador'] = localizador_match.group(1)

        # Extraer Agencia
        agencia_match = re.search(r'Agencia:\s*([^\n]+)', text, re.IGNORECASE)
        if agencia_match:
            data['agencia'] = agencia_match.group(1).strip()

        # Extraer Fecha de Emisión
        fecha_emision_match = re.search(r'Fecha\s+Emision:\s*([^\n]+)', text, re.IGNORECASE)
        if fecha_emision_match:
            fecha_emision_str = fecha_emision_match.group(1).strip()
            # Si dice "INMEDIATO" o está vacío, usar None (se usará fecha del correo como fallback)
            if fecha_emision_str.upper() == "INMEDIATO" or not fecha_emision_str:
                data['fecha_emision'] = None
                self.logger.info(f"📅 Fecha emisión: INMEDIATO - se usará fecha de llegada del correo")
            else:
                # Intentar parsear la fecha, si falla guardar como None
                data['fecha_emision'] = self._parse_spanish_date(fecha_emision_str)
                if data['fecha_emision']:
                    self.logger.info(f"📅 Fecha emisión extraída: {data['fecha_emision']}")
                else:
                    self.logger.warning(f"⚠️  No se pudo parsear fecha emisión: {fecha_emision_str}")

        # Extraer Nombre del Hotel
        hotel_match = re.search(r'(.*?Hotel.*?)(?=\n|Total:)', text, re.IGNORECASE)
        if hotel_match:
            data['nombre_hotel'] = hotel_match.group(1).strip()

        # Extraer Dirección
        direccion_match = re.search(r'Av\.\s+[^\n]+|[^\n]+,\s+\d+\s+[A-Za-z\s]+,', text)
        if direccion_match:
            data['direccion_hotel'] = direccion_match.group(0).strip()

        # Extraer Teléfono
        telefono_match = re.search(r'Teléfono:\s*(\d+)', text, re.IGNORECASE)
        if telefono_match:
            data['telefono_hotel'] = telefono_match.group(1)

        # Extraer Total (monto) - MÚLTIPLES FORMATOS SOPORTADOS
        # Patrones para detectar el monto total en diferentes formatos
        monto_patterns = [
            r'Total:\s*CLP\s*\$?\s*([\d,.]+)',           # Total: CLP 123456 o Total: CLP $123.456
            r'Total:\s*\$\s*([\d,.]+)',                  # Total: $123.456
            r'Monto\s+Total:\s*CLP\s*\$?\s*([\d,.]+)',   # Monto Total: CLP 123456
            r'Monto\s+Total:\s*\$\s*([\d,.]+)',          # Monto Total: $123.456
            r'Monto:\s*CLP\s*\$?\s*([\d,.]+)',           # Monto: CLP 123456
            r'Monto:\s*\$\s*([\d,.]+)',                  # Monto: $123.456
            r'Total\s+a\s+Pagar:\s*CLP\s*\$?\s*([\d,.]+)',  # Total a Pagar: CLP 123456
            r'Total\s+a\s+Pagar:\s*\$\s*([\d,.]+)',      # Total a Pagar: $123.456
            r'Precio\s+Total:\s*CLP\s*\$?\s*([\d,.]+)',  # Precio Total: CLP 123456
            r'Precio\s+Total:\s*\$\s*([\d,.]+)',         # Precio Total: $123.456
            r'CLP\s*\$?\s*([\d,.]+)\s*(?:Total|Monto)',  # CLP 123456 Total
            r'Total.*?CLP\s*\$?\s*([\d,.]+)',            # Total ... CLP 123456
            r'(?:Total|Monto).*?\$\s*([\d,.]+)',         # Total/Monto ... $123.456
        ]

        for pattern in monto_patterns:
            total_match = re.search(pattern, text, re.IGNORECASE)
            if total_match:
                monto_str = total_match.group(1).replace(',', '').replace('.', '')
                try:
                    # Convertir el monto
                    # Si el formato original tenía punto como separador de miles (ej: 123.456)
                    # se eliminó y quedó 123456, lo cual es correcto
                    data['monto_total'] = float(monto_str)
                    data['moneda'] = 'CLP'
                    self.logger.info(f"💰 Monto extraído: CLP {data['monto_total']} (patrón: {pattern[:30]}...)")
                    break  # Salir del loop si encontramos un monto válido
                except ValueError:
                    self.logger.warning(f"No se pudo convertir monto: {total_match.group(1)}")
                    continue  # Intentar con el siguiente patrón

        # Si no se encontró con ningún patrón, intentar buscar cualquier número grande precedido de CLP o $
        if 'monto_total' not in data:
            fallback_match = re.search(r'(?:CLP|\$)\s*\$?\s*([\d,.]{5,})', text, re.IGNORECASE)
            if fallback_match:
                monto_str = fallback_match.group(1).replace(',', '').replace('.', '')
                try:
                    data['monto_total'] = float(monto_str)
                    data['moneda'] = 'CLP'
                    self.logger.info(f"💰 Monto extraído (fallback): CLP {data['monto_total']}")
                except ValueError:
                    pass

        # Extraer Check-in
        checkin_match = re.search(
            r'Check\s+In:\s*([a-záéíóú]+)\s+(\d+),\s+([a-záéíóú]+)\.?\s+(\d{4})',
            text,
            re.IGNORECASE
        )
        if checkin_match:
            fecha_str = f"{checkin_match.group(2)} {checkin_match.group(3)} {checkin_match.group(4)}"
            data['fecha_checkin'] = self._parse_spanish_date(fecha_str)

        # Extraer Check-out
        checkout_match = re.search(
            r'Check\s+Out:\s*([a-záéíóú]+)\s+(\d+),\s+([a-záéíóú]+)\.?\s+(\d{4})',
            text,
            re.IGNORECASE
        )
        if checkout_match:
            fecha_str = f"{checkout_match.group(2)} {checkout_match.group(3)} {checkout_match.group(4)}"
            data['fecha_checkout'] = self._parse_spanish_date(fecha_str)

        # Extraer Hora de Llegada
        hora_llegada_match = re.search(r'Hora\s+Llegada:\s*(\d+:\d+\s*[AP]M)', text, re.IGNORECASE)
        if hora_llegada_match:
            data['hora_llegada'] = hora_llegada_match.group(1)

        # Extraer Hora de Salida
        hora_salida_match = re.search(r'Hora\s+Salida:\s*(\d+:\d+\s*[AP]M)', text, re.IGNORECASE)
        if hora_salida_match:
            data['hora_salida'] = hora_salida_match.group(1)

        # Extraer Número de Noches
        noches_match = re.search(r'Noches:\s*(\d+)', text, re.IGNORECASE)
        if noches_match:
            data['numero_noches'] = int(noches_match.group(1))

        # Extraer Número de Habitaciones
        habitaciones_match = re.search(r'Habitaciones:\s*(\d+)', text, re.IGNORECASE)
        if habitaciones_match:
            data['numero_habitaciones'] = int(habitaciones_match.group(1))

        # Extraer Límite de Cancelación
        cancelacion_match = re.search(
            r'([a-záéíóú]+),\s+(\d+)\s+de\s+([a-záéíóú]+)\s+de\s+(\d{4})',
            text,
            re.IGNORECASE
        )
        if cancelacion_match:
            fecha_str = f"{cancelacion_match.group(2)} {cancelacion_match.group(3)} {cancelacion_match.group(4)}"
            data['fecha_limite_cancelacion'] = self._parse_spanish_date(fecha_str)

        # Extraer detalles de habitaciones
        data['detalles_habitaciones'] = self._extract_room_details(text)

        # Extraer Observaciones
        observaciones_match = re.search(
            r'Observaciones\s*\n\s*([^\n]*)\s*Sin\s+notas\s+de\s+hotel\s+informadas\.\s*([^\n]*)',
            text,
            re.IGNORECASE
        )
        if observaciones_match and observaciones_match.group(1).strip():
            data['observaciones_hotel'] = observaciones_match.group(1).strip()

        # Extraer Notas del Asesor
        notas_match = re.search(
            r'Notas\s+del\s+asesor\s*\n\s*([^\n]*)\s*Sin\s+notas\s+del\s+asesor\s+informadas\.\s*([^\n]*)',
            text,
            re.IGNORECASE
        )
        if notas_match and notas_match.group(1).strip():
            data['notas_asesor'] = notas_match.group(1).strip()

        self.logger.info(f"Datos extraídos: ID={data.get('id_reserva')}, Agencia={data.get('agencia')}")

        return data

    def _extract_room_details(self, text: str) -> str:
        """Extrae detalles de las habitaciones y los serializa a JSON"""
        habitaciones = []

        # Buscar patrones de habitaciones
        habitacion_pattern = re.compile(
            r'Habitación\s+(\d+)\s*‐\s*Categoría\s*‐\s*([^\‐]+)\‐\s*ADT/CHD:\s*(\d+)/(\d+)\s*‐\s*Plan\s+Alimentación:\s*([^\n]+)',
            re.IGNORECASE
        )

        for match in habitacion_pattern.finditer(text):
            habitacion = {
                'numero': int(match.group(1)),
                'categoria': match.group(2).strip(),
                'adultos': int(match.group(3)),
                'ninos': int(match.group(4)),
                'plan_alimentacion': match.group(5).strip(),
                'huespedes': []
            }

            # Buscar huéspedes de esta habitación
            # (esto es más complejo y puede requerir ajustes según el formato exacto)
            habitaciones.append(habitacion)

        return json.dumps(habitaciones, ensure_ascii=False) if habitaciones else None

    def _parse_spanish_date(self, fecha_str: str) -> Optional[datetime]:
        """
        Convierte fecha en español a datetime
        Ej: "27 nov. 2025" -> datetime
        """
        meses = {
            'ene': 1, 'enero': 1,
            'feb': 2, 'febrero': 2,
            'mar': 3, 'marzo': 3,
            'abr': 4, 'abril': 4,
            'may': 5, 'mayo': 5,
            'jun': 6, 'junio': 6,
            'jul': 7, 'julio': 7,
            'ago': 8, 'agosto': 8,
            'sep': 9, 'septiembre': 9,
            'oct': 10, 'octubre': 10,
            'nov': 11, 'noviembre': 11,
            'dic': 12, 'diciembre': 12
        }

        try:
            # Normalizar
            fecha_str = fecha_str.lower().strip().replace('.', '')

            # Extraer partes
            parts = fecha_str.split()
            if len(parts) >= 3:
                dia = int(parts[0])
                mes_str = parts[1]
                anio = int(parts[2])

                # Buscar mes
                mes = meses.get(mes_str)
                if mes:
                    return datetime(anio, mes, dia)

        except Exception as e:
            self.logger.warning(f"Error parseando fecha '{fecha_str}': {e}")

        return None

    def validate_data(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Valida que los datos extraídos sean completos y correctos

        Returns:
            (es_valido, lista_de_errores)
        """
        errors = []

        # Campos obligatorios
        required_fields = ['id_reserva', 'loc_interno', 'agencia', 'monto_total']

        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Campo obligatorio faltante: {field}")

        # Validaciones de tipo
        if 'monto_total' in data:
            try:
                float(data['monto_total'])
            except (ValueError, TypeError):
                errors.append("Monto total no es un número válido")

        if 'fecha_checkin' in data and data['fecha_checkin']:
            if not isinstance(data['fecha_checkin'], datetime):
                errors.append("fecha_checkin no es un datetime válido")

        if 'fecha_checkout' in data and data['fecha_checkout']:
            if not isinstance(data['fecha_checkout'], datetime):
                errors.append("fecha_checkout no es un datetime válido")

        is_valid = len(errors) == 0

        if is_valid:
            self.logger.info(f"✅ Datos validados correctamente para reserva {data.get('id_reserva')}")
        else:
            self.logger.error(f"❌ Errores de validación: {', '.join(errors)}")

        return is_valid, errors


# Instancia global
pdf_processor = PDFProcessor()


if __name__ == "__main__":
    # Test con el PDF de ejemplo
    import sys

    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        # Buscar PDF en carpeta data/
        pdf_path = Path(__file__).parent.parent / "data" / "resumen del servicio.pdf"

    processor = PDFProcessor()
    data = processor.extract_from_file(pdf_path)

    if data:
        print("\n=== Datos Extraídos ===")
        for key, value in data.items():
            print(f"{key}: {value}")

        is_valid, errors = processor.validate_data(data)
        print(f"\n=== Validación ===")
        print(f"Válido: {is_valid}")
        if errors:
            print(f"Errores: {', '.join(errors)}")
    else:
        print("❌ No se pudieron extraer datos del PDF")
