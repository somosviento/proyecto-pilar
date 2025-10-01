/**
 * Función principal que actúa como endpoint para recibir solicitudes POST.
 * Es el controlador central de la API.
 * @param {Object} e - Objeto de evento que contiene los datos de la solicitud.
 * @returns {ContentService} - Respuesta JSON con los resultados.
 */
function doPost(e) {
  try {
    // 1. Parsear los datos JSON recibidos en la solicitud.
    const data = JSON.parse(e.postData.contents);
    
    // 2. Validar el token de seguridad para proteger el endpoint.
    if (!validateSecurityToken(data.token)) {
      return createResponse(false, 'Token de seguridad inválido o no proporcionado', null, 401);
    }
    
    // 3. Validar que se haya proporcionado una acción a ejecutar.
    if (!data.action) {
      return createResponse(false, 'Acción no especificada', null);
    }

    // 4. Ejecutar la acción correspondiente usando un switch.
    // Este es el enrutador principal de la API.
    switch (data.action) {
      case 'createFolders':
        return handleCreateFolders(data);
        
      case 'generateDocuments':
        return handleGenerateDocuments(data);
        
      case 'sendEmail':
        return handleSendEmail(data);

      case 'uploadFiles':
        return handleFileUpload(data);

      case 'getMimeType': // <-- AÑADE ESTA LÍNEA
        return handleGetMimeType(data); // <-- AÑADE ESTA LÍNEA
      // --------------------------------
        
      default:
        // Si la acción no coincide con ninguna de las anteriores, devolver un error.
        return createResponse(false, 'Acción no válida: ' + data.action, null);
    }
    
  } catch (error) {
    // Si ocurre cualquier error inesperado (ej. JSON mal formado), se captura aquí.
    console.error('Error fatal en doPost:', error);
    return createResponse(false, 'Error interno del servidor: ' + error.message, null);
  }
}

/**
 * Maneja la creación de carpetas y subcarpetas
 * @param {Object} data - Datos de la solicitud
 * @returns {ContentService} - Respuesta JSON
 */
function handleCreateFolders(data) {
  try {
    // Validar datos requeridos
    if (!data.rootFolderId) {
      return createResponse(false, 'ID de carpeta raíz no proporcionado', null);
    }
    
    if (!data.folders || !Array.isArray(data.folders) || data.folders.length === 0) {
      return createResponse(false, 'Lista de carpetas no proporcionada o vacía', null);
    }
    
    // Verificar que la carpeta raíz existe
    let rootFolder;
    try {
      rootFolder = DriveApp.getFolderById(data.rootFolderId);
    } catch (error) {
      return createResponse(false, 'Carpeta raíz no encontrada: ' + data.rootFolderId, null);
    }
    
    // Crear las carpetas
    const createdFolders = createFoldersStructure(rootFolder, data.folders);
    
    return createResponse(true, 'Carpetas creadas exitosamente', {
      rootFolderId: data.rootFolderId,
      createdFolders: createdFolders
    });
    
  } catch (error) {
    console.error('Error en handleCreateFolders:', error);
    return createResponse(false, 'Error al crear carpetas: ' + error.message, null);
  }
}

/**
 * Crea la estructura de carpetas recursivamente
 * @param {DriveApp.Folder} parentFolder - Carpeta padre
 * @param {Array} folders - Lista de carpetas a crear
 * @returns {Array} - Lista de carpetas creadas con sus IDs
 */
function createFoldersStructure(parentFolder, folders) {
  const createdFolders = [];
  
  folders.forEach(folderData => {
    try {
      // Validar que el nombre de la carpeta esté presente
      if (!folderData.name || folderData.name.trim() === '') {
        console.warn('Nombre de carpeta vacío, omitiendo...');
        return;
      }
      
      // Verificar si la carpeta ya existe
      const existingFolders = parentFolder.getFoldersByName(folderData.name);
      let currentFolder;
      
      if (existingFolders.hasNext()) {
        // Si ya existe, usar la existente
        currentFolder = existingFolders.next();
        console.log('Carpeta ya existe: ' + folderData.name);
      } else {
        // Crear nueva carpeta
        currentFolder = parentFolder.createFolder(folderData.name);
        console.log('Carpeta creada: ' + folderData.name);
      }
      
      const folderInfo = {
        name: folderData.name,
        id: currentFolder.getId(),
        url: currentFolder.getUrl(),
        existed: existingFolders.hasNext()
      };
      
      // Si hay subcarpetas, crearlas recursivamente
      if (folderData.subfolders && Array.isArray(folderData.subfolders) && folderData.subfolders.length > 0) {
        folderInfo.subfolders = createFoldersStructure(currentFolder, folderData.subfolders);
      }
      
      createdFolders.push(folderInfo);
      
    } catch (error) {
      console.error('Error al crear carpeta ' + folderData.name + ':', error);
      createdFolders.push({
        name: folderData.name,
        error: error.message
      });
    }
  });
  
  return createdFolders;
}

/**
 * Valida el token de seguridad
 * @param {string} providedToken - Token proporcionado en la solicitud
 * @returns {boolean} - True si el token es válido, false en caso contrario
 */
function validateSecurityToken(providedToken) {
  try {
    // Obtener el token seguro de las propiedades del script
    const secureToken = PropertiesService.getScriptProperties().getProperty('SECURE_TOKEN');
    
    if (!secureToken) {
      console.error('Token de seguridad no configurado en las propiedades del script');
      return false;
    }
    
    if (!providedToken) {
      console.warn('Token no proporcionado en la solicitud');
      return false;
    }
    
    // Comparar tokens de forma segura
    return providedToken === secureToken;
    
  } catch (error) {
    console.error('Error al validar token de seguridad:', error);
    return false;
  }
}

/**
 * Crea una respuesta JSON estandarizada
 * @param {boolean} success - Indica si la operación fue exitosa
 * @param {string} message - Mensaje descriptivo
 * @param {Object} data - Datos adicionales de la respuesta
 * @param {number} statusCode - Código de estado HTTP (opcional)
 * @returns {ContentService} - Respuesta JSON
 */
function createResponse(success, message, data, statusCode) {
  const response = {
    success: success,
    message: message,
    timestamp: new Date().toISOString(),
    data: data
  };
  
  // Si se proporciona un código de error, agregarlo a la respuesta
  if (statusCode && !success) {
    response.statusCode = statusCode;
  }
  
  return ContentService
    .createTextOutput(JSON.stringify(response))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Maneja la generación de documentos a partir de plantillas
 * @param {Object} data - Datos de la solicitud
 * @returns {ContentService} - Respuesta JSON
 */
function handleGenerateDocuments(data) {
  try {
    // Validar datos requeridos
    if (!data.documents || !Array.isArray(data.documents) || data.documents.length === 0) {
      return createResponse(false, 'Lista de documentos no proporcionada o vacía', null);
    }
    
    const generatedDocuments = [];
    
    // Procesar cada documento a generar
    for (const docData of data.documents) {
      try {
        const result = generateDocumentFromTemplate(docData);
        generatedDocuments.push(result);
      } catch (error) {
        console.error('Error al generar documento:', error);
        generatedDocuments.push({
          templateId: docData.templateId,
          fileName: docData.fileName || 'Sin nombre',
          error: error.message,
          success: false
        });
      }
    }
    
    return createResponse(true, 'Procesamiento de documentos completado', {
      totalRequested: data.documents.length,
      totalSuccess: generatedDocuments.filter(doc => doc.success).length,
      totalErrors: generatedDocuments.filter(doc => !doc.success).length,
      documents: generatedDocuments
    });
    
  } catch (error) {
    console.error('Error en handleGenerateDocuments:', error);
    return createResponse(false, 'Error al generar documentos: ' + error.message, null);
  }
}

/**
 * Genera un documento individual a partir de una plantilla usando makeCopy().
 * @param {Object} docData - Datos del documento a generar.
 * @returns {Object} - Información del documento generado.
 */
function generateDocumentFromTemplate(docData) {
  // --- SELLO DE DIAGNÓSTICO ---
  console.log("EJECUTANDO VERSIÓN SIMPLE (makeCopy) - Después de activar las APIs.");
  // -----------------------------

  // 1. Validar datos requeridos
  if (!docData.templateId) {
    throw new Error('ID de plantilla no proporcionado');
  }
  if (!docData.fileName) {
    throw new Error('Nombre del archivo no proporcionado');
  }
  
  // 2. Verificar que la plantilla existe
  let templateDocFile;
  try {
    templateDocFile = DriveApp.getFileById(docData.templateId);
  } catch (error) {
    throw new Error('Plantilla no encontrada: ' + docData.templateId);
  }
  
  // 3. Reemplazar placeholders en el nombre del archivo
  const finalFileName = replacePlaceholdersInString(docData.fileName, docData.fields || {});
  
  // 4. Hacer una copia de la plantilla usando el nombre de archivo procesado.
  //    Esta es la línea que estamos volviendo a probar.
  const newDocFile = templateDocFile.makeCopy(finalFileName);
  
  // 5. Mover el documento si se especifica una carpeta de destino
  if (docData.folderId) {
    try {
      const folder = DriveApp.getFolderById(docData.folderId);
      const parents = newDocFile.getParents();
      while (parents.hasNext()) {
        parents.next().removeFile(newDocFile);
      }
      folder.addFile(newDocFile);
    } catch (error) {
      console.warn('No se pudo mover el archivo a la carpeta especificada:', error.message);
    }
  }
  
  // 6. Reemplazar campos en el cuerpo del documento si se proporcionan
  if (docData.fields && Object.keys(docData.fields).length > 0) {
    replaceFieldsInDocument(newDocFile.getId(), docData.fields, docData.signatureData, docData.equipoData);
  }
  
  // 7. Devolver la información del documento creado
  return {
    success: true,
    templateId: docData.templateId,
    fileName: finalFileName,
    documentId: newDocFile.getId(),
    documentUrl: newDocFile.getUrl(),
    folderId: docData.folderId || null,
    fieldsReplaced: docData.fields ? Object.keys(docData.fields).length : 0
  };
}

/**
 * Reemplaza campos en un documento de Google Docs con soporte para inserción de imágenes de firma y tablas de equipo
 * @param {string} documentId - ID del documento.
 * @param {Object} fields - Objeto con los campos a reemplazar.
 * @param {string} signatureData - Datos de firma en base64 (opcional).
 * @param {Array} equipoData - Datos del equipo (opcional).
 */
function replaceFieldsInDocument(documentId, fields, signatureData, equipoData) {
  try {
    const doc = DocumentApp.openById(documentId);
    const body = doc.getBody();

    // Función auxiliar para procesar un elemento que contiene texto.
    const processElement = (element) => {
      let originalText = element.getText();
      
      if (!originalText) {
        return;
      }
      
      let modifiedText = originalText;

      // Realizamos los reemplazos en la cadena de texto.
      for (const [key, value] of Object.entries(fields)) {
        const placeholder = `[[${key}]]`;
        modifiedText = modifiedText.split(placeholder).join(value || '');
      }

      // Solo si el texto ha cambiado, lo vaciamos y reescribimos.
      if (originalText !== modifiedText) {
        element.clear();
        element.appendText(modifiedText);
      }
    };

    // Procesar todos los párrafos y tablas
    body.getParagraphs().forEach(processElement);
    body.getTables().forEach(table => {
      for (let r = 0; r < table.getNumRows(); r++) {
        for (let c = 0; c < table.getRow(r).getNumCells(); c++) {
          processElement(table.getCell(r, c));
        }
      }
    });

    // Insertar tabla de equipo si existe
    if (equipoData && equipoData.length > 0) {
      insertTeamTableInDocument(doc, equipoData);
    }

    // Insertar imagen de firma si existe
    if (signatureData && signatureData.startsWith('data:image/')) {
      insertSignatureInDocument(doc, signatureData);
    }

    doc.saveAndClose();
    console.log('Reemplazo de campos completado para el documento ID: ' + documentId);

  } catch (error) {
    console.error('Error al reemplazar campos en documento:', error);
    throw new Error('Error al procesar reemplazos en el documento: ' + error.message);
  }
}

/**
 * Inserta una tabla del equipo en el documento (incluye claustro)
 * @param {DocumentApp.Document} doc - El documento donde insertar la tabla
 * @param {Array} equipoData - Array con los datos del equipo
 */
function insertTeamTableInDocument(doc, equipoData) {
  try {
    console.log('Insertando tabla de equipo en el documento');
    console.log('Datos del equipo recibidos:', equipoData);
    
    const body = doc.getBody();
    const searchResult = body.findText('[[EQUIPO]]');
    
    console.log('Resultado de búsqueda del placeholder [[EQUIPO]]:', searchResult);
    
    if (searchResult) {
      // Obtener el elemento que contiene el placeholder
      const element = searchResult.getElement();
      const paragraph = element.getParent();
      
      // Encontrar la posición exacta del texto
      const startOffset = searchResult.getStartOffset();
      const endOffset = searchResult.getEndOffsetInclusive();
      
      // Reemplazar el texto del placeholder
      if (element.getType() === DocumentApp.ElementType.TEXT) {
        element.asText().deleteText(startOffset, endOffset);
      }
      
      // Crear la tabla con encabezados (ahora incluye Claustro)
      const tableData = [
        ['Apellido y Nombre', 'DNI', 'Correo Electrónico', 'Claustro']
      ];
      
      // Agregar filas de datos del equipo
      equipoData.forEach(miembro => {
        tableData.push([
          miembro.apellido_nombre || '',
          miembro.dni || '',
          miembro.correo || '',
          miembro.claustro || ''
        ]);
      });
      
      // Insertar la tabla en el documento
      const table = paragraph.getParent().insertTable(paragraph.getChildIndex(paragraph), tableData);
      
      // Aplicar formato a la tabla
      formatTeamTable(table);
      
      // Eliminar el párrafo original que contenía el placeholder
      paragraph.removeFromParent();
      
      console.log('Tabla de equipo insertada exitosamente');
      return true;
      
    } else {
      console.log('No se encontró el placeholder [[EQUIPO]] en el documento');
      return false;
    }
    
  } catch (error) {
    console.error('Error insertando tabla de equipo:', error);
    return false;
  }
}

/**
 * Aplica formato a la tabla del equipo
 * @param {DocumentApp.Table} table - La tabla a formatear
 */
function formatTeamTable(table) {
  try {
    // Formatear encabezado (primera fila)
    const headerRow = table.getRow(0);
    headerRow.setBackgroundColor('#4472C4'); // Azul
    
    for (let c = 0; c < headerRow.getNumCells(); c++) {
      const cell = headerRow.getCell(c);
      const text = cell.getChild(0).asText();
      text.setForegroundColor('#FFFFFF'); // Texto blanco
      text.setBold(true);
      cell.setPaddingTop(8);
      cell.setPaddingBottom(8);
      cell.setPaddingLeft(8);
      cell.setPaddingRight(8);
    }
    
    // Formatear filas de datos
    for (let r = 1; r < table.getNumRows(); r++) {
      const row = table.getRow(r);
      
      // Alternar colores de fondo
      if (r % 2 === 0) {
        row.setBackgroundColor('#F2F2F2'); // Gris claro
      } else {
        row.setBackgroundColor('#FFFFFF'); // Blanco
      }
      
      // Aplicar padding a todas las celdas
      for (let c = 0; c < row.getNumCells(); c++) {
        const cell = row.getCell(c);
        cell.setPaddingTop(6);
        cell.setPaddingBottom(6);
        cell.setPaddingLeft(8);
        cell.setPaddingRight(8);
      }
    }
    
    // Aplicar bordes a toda la tabla
    table.setBorderWidth(1);
    table.setBorderColor('#000000');
    
    console.log('Formato aplicado a la tabla de equipo');
    
  } catch (error) {
    console.error('Error aplicando formato a la tabla:', error);
  }
}

/**
 * Inserta una imagen de firma en el documento
 * @param {DocumentApp.Document} doc - El documento donde insertar la firma
 * @param {string} signatureData - Datos de la imagen en formato base64
 */
function insertSignatureInDocument(doc, signatureData) {
  try {
    console.log('Insertando imagen de firma en el documento');
    
    // Buscar el placeholder de firma en todo el documento
    const body = doc.getBody();
    const searchResult = body.findText('[[CUADRO_FIRMA]]');
    
    console.log('Resultado de búsqueda del placeholder [[CUADRO_FIRMA]]:', searchResult);
    
    if (searchResult) {
      // Extraer los datos base64 de la imagen
      const base64Data = signatureData.split(',')[1];
      const imageBlob = Utilities.newBlob(
        Utilities.base64Decode(base64Data),
        'image/png',
        'firma.png'
      );
      
      // Obtener el elemento que contiene el placeholder
      const element = searchResult.getElement();
      const paragraph = element.getParent();
      
      // Encontrar la posición exacta del texto
      const startOffset = searchResult.getStartOffset();
      const endOffset = searchResult.getEndOffsetInclusive();
      
      // Reemplazar el texto del placeholder con texto vacío
      if (element.getType() === DocumentApp.ElementType.TEXT) {
        element.asText().deleteText(startOffset, endOffset);
      }
      
      // Insertar la imagen en el párrafo
      const image = paragraph.asParagraph().insertInlineImage(startOffset, imageBlob);
      
      // Redimensionar la imagen a un tamaño apropiado
      const maxWidth = 200; // píxeles
      const maxHeight = 100; // píxeles
      
      image.setWidth(maxWidth);
      image.setHeight(maxHeight);
      
      // Agregar texto descriptivo después de la imagen
      paragraph.asParagraph().appendText('\nFirma del Docente Responsable');
      
      console.log('Imagen de firma insertada exitosamente');
      return true;
      
    } else {
      console.log('No se encontró el placeholder [[CUADRO_FIRMA]] en el documento');
      return false;
    }
    
  } catch (error) {
    console.error('Error insertando imagen de firma:', error);
    return false;
  }
}

/**
 * Maneja el envío de correos, usando UrlFetchApp para forzar la conversión
 * a Word o PDF, y aplicando correctamente el senderName.
 * @param {Object} data - Datos de la solicitud.
 * @returns {ContentService} - Respuesta JSON.
 */
function handleSendEmail(data) {
  try {
    // 1. Validar datos requeridos básicos
    if (!data.to) return createResponse(false, 'El destinatario (to) es obligatorio.', null);
    if (!data.subject) return createResponse(false, 'El asunto (subject) es obligatorio.', null);
    if (!data.htmlBody) return createResponse(false, 'El cuerpo del correo (htmlBody) es obligatorio.', null);

    // 2. Preparar las opciones avanzadas del correo
    const mailOptions = {
      htmlBody: data.htmlBody,
      attachments: [],
      inlineImages: {}
    };
    
    // --- LÓGICA CORREGIDA PARA LAS OPCIONES ---
    if (data.senderName) mailOptions.name = data.senderName; // <-- ¡ESTA ES LA LÍNEA IMPORTANTE!
    if (data.replyTo) mailOptions.replyTo = data.replyTo;
    if (data.cc) mailOptions.cc = data.cc;
    if (data.bcc) mailOptions.bcc = data.bcc;
    // ------------------------------------------

    const processedFiles = [];
    const failedFiles = [];

    // 3. Procesar la lista unificada de archivos adjuntos (esta parte ya funciona)
    if (data.attachments && Array.isArray(data.attachments)) {
      for (const attachmentConfig of data.attachments) {
        if (!attachmentConfig.fileId) { /* ... */ continue; }
        try {
          // ... (La lógica de UrlFetchApp que ya solucionamos no cambia)
          const file = DriveApp.getFileById(attachmentConfig.fileId);
          let finalBlob;
          let finalName = file.getName();
          let conversionType = 'original';

          if (attachmentConfig.convertTo) {
            let mimeType, extension;
            if (attachmentConfig.convertTo.toLowerCase() === 'word') {
              mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
              extension = '.docx';
              conversionType = 'word';
            } else if (attachmentConfig.convertTo.toLowerCase() === 'pdf') {
              mimeType = 'application/pdf';
              extension = '.pdf';
            }
            if (mimeType) {
              const url = `https://www.googleapis.com/drive/v3/files/${attachmentConfig.fileId}/export?mimeType=${mimeType}`;
              const token = ScriptApp.getOAuthToken();
              const response = UrlFetchApp.fetch(url, {
                headers: { 'Authorization': 'Bearer ' + token },
                muteHttpExceptions: true
              });
              if (response.getResponseCode() !== 200) {
                throw new Error(`La API de exportación devolvió un error: ${response.getContentText()}`);
              }
              finalBlob = response.getBlob();
              if (!finalName.toLowerCase().endsWith(extension)) {
                finalName += extension;
              }
            }
          }

          if (!finalBlob) finalBlob = file.getBlob();
          finalBlob.setName(finalName);
          mailOptions.attachments.push(finalBlob);
          processedFiles.push({ id: attachmentConfig.fileId, name: finalName, conversion: conversionType });

        } catch (e) {
          const errorMessage = 'Fallo al procesar adjunto. Error: ' + e.message;
          failedFiles.push({ id: attachmentConfig.fileId, error: errorMessage, requestedConversion: attachmentConfig.convertTo || 'original' });
        }
      }
    }
    
    // 4. Validar si fallaron los adjuntos
    if (failedFiles.length > 0) {
      return createResponse(false, 'Error crítico al procesar adjuntos. El correo NO fue enviado.', { failedFiles });
    }
    
    // 5. Enviar el correo electrónico
    const plainTextBody = data.plainTextBody || data.htmlBody.replace(/<[^>]*>/g, "");
    GmailApp.sendEmail(data.to, data.subject, plainTextBody, mailOptions);

    return createResponse(true, 'Correo enviado exitosamente.', { processedFiles });

  } catch (error) {
    console.error('Error fatal en handleSendEmail:', error);
    return createResponse(false, 'Error al enviar el correo: ' + error.message, null);
  }
}

/**
 * Reemplaza placeholders en una cadena de texto.
 * @param {string} text - El texto que contiene placeholders, ej. "Contrato para [[NOMBRE_CLIENTE]]".
 * @param {Object} fields - El objeto con los valores de reemplazo, ej. { 'NOMBRE_CLIENTE': 'Juan Pérez' }.
 * @returns {string} - El texto con los placeholders reemplazados.
 */
function replacePlaceholdersInString(text, fields) {
  if (!fields || !text) {
    return text || '';
  }

  let processedText = text;
  for (const [key, value] of Object.entries(fields)) {
    // Usamos una Expresión Regular con el flag 'g' para reemplazar todas las ocurrencias.
    const placeholder = new RegExp(`\\[\\[${key}\\]\\]`, 'g');
    processedText = processedText.replace(placeholder, value || '');
  }
  return processedText;
}


/**
 * Maneja la subida de uno o más archivos a Google Drive.
 * Los archivos deben venir codificados en Base64.
 * @param {Object} data - Datos de la solicitud.
 * @returns {ContentService} - Respuesta JSON.
 */
function handleFileUpload(data) {
  try {
    // 1. Validar que la lista de archivos exista y sea un array
    if (!data.files || !Array.isArray(data.files) || data.files.length === 0) {
      return createResponse(false, 'Lista de archivos (files) no proporcionada o vacía.', null);
    }

    const uploadResults = [];

    // 2. Procesar cada archivo en la lista
    for (const fileData of data.files) {
      try {
        // 3. Validar los datos de cada archivo individual
        if (!fileData.fileName) throw new Error('El campo "fileName" es obligatorio para cada archivo.');
        if (!fileData.mimeType) throw new Error('El campo "mimeType" es obligatorio para cada archivo.');
        if (!fileData.fileContent) throw new Error('El campo "fileContent" (Base64) es obligatorio para cada archivo.');
        
        // 4. Decodificar el contenido del archivo de Base64 a bytes
        const decodedContent = Utilities.base64Decode(fileData.fileContent);
        
        // 5. Crear un "Blob" de datos que Google Drive pueda usar
        const fileBlob = Utilities.newBlob(decodedContent, fileData.mimeType, fileData.fileName);

        let destinationFolder;
        let parentFolderId = null;

        // 6. Encontrar la carpeta de destino si se proporciona un ID
        if (fileData.folderId) {
          try {
            destinationFolder = DriveApp.getFolderById(fileData.folderId);
            parentFolderId = fileData.folderId;
          } catch (e) {
            throw new Error('La carpeta de destino con ID "' + fileData.folderId + '" no fue encontrada.');
          }
        }
        
        // 7. Crear el archivo en la ubicación correcta
        const newFile = destinationFolder 
          ? destinationFolder.createFile(fileBlob) 
          : DriveApp.createFile(fileBlob); // Si no hay carpeta, se sube a la raíz

        uploadResults.push({
          success: true,
          fileName: newFile.getName(),
          fileId: newFile.getId(),
          fileUrl: newFile.getUrl(),
          folderId: parentFolderId
        });

      } catch (error) {
        // Capturar errores para un archivo individual sin detener el proceso
        console.error('Error al subir el archivo ' + (fileData.fileName || '') + ':', error);
        uploadResults.push({
          success: false,
          fileName: fileData.fileName || 'Nombre no especificado',
          error: error.message
        });
      }
    }

    // 8. Devolver una respuesta con el resumen de todas las subidas
    return createResponse(true, 'Procesamiento de subida de archivos completado.', {
      totalRequested: data.files.length,
      totalSuccess: uploadResults.filter(r => r.success).length,
      totalErrors: uploadResults.filter(r => !r.success).length,
      results: uploadResults
    });

  } catch (error) {
    console.error('Error en handleFileUpload:', error);
    return createResponse(false, 'Error al procesar la subida de archivos: ' + error.message, null);
  }
}




