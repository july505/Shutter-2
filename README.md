# Shutter PR - APK

Aplicación Android para llevar el control de cargadores.

## Precios

### Pistola grande
- Primer cargador: 800 CUP
- Cada cargador adicional: 700 CUP

### Pistola pequeña
- Primer cargador: 500 CUP
- Cada cargador adicional: 400 CUP

## Funciones

- Añadir cargador grande.
- Añadir cargador pequeño.
- Deshacer una venta.
- Ver recaudación por tipo.
- Ver total de cargadores.
- Ver total de dinero.
- Reiniciar el control.
- Guardar automáticamente los datos en el teléfono.

## Compilar la APK

La forma recomendada es usar Linux/Ubuntu o WSL2 en Windows.

Instalar dependencias:

    sudo apt update
    sudo apt install -y python3-pip git zip unzip openjdk-17-jdk

Instalar Buildozer:

    pip3 install --user buildozer

Entrar en la carpeta del proyecto:

    cd ShutterPR

Crear la APK de prueba:

    buildozer android debug

La APK aparecerá en la carpeta `bin/`.

Para una compilación posterior:

    buildozer android clean
    buildozer android debug

## Importante

La aplicación guarda los contadores localmente en `shutter_pr.json`. Al cerrar y volver a abrir la aplicación, los datos permanecen.

La opción "Reiniciar control" borra los contadores actuales después de una confirmación.
