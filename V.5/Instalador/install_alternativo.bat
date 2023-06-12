ECHO OFF
echo У######################################################Ф
echo У###          ACTUAL Montagens e Automacao          ###Ф
echo У###         ==============================         ###Ф
echo У###                                                ###Ф
echo У###     SCRIPT Para instalacao do supervisorio     ###Ф
echo У###     Vc precisa estar conectado a internet!!    ###Ф
echo У###                                                ###Ф
echo У######################################################Ф
pause
CLS
echo У######################################################Ф
echo У###                                                ###Ф
echo У###  Vamos iniciar configurando a base do sistema  ###Ф
echo У###                Install Python 2.7              ###Ф
echo У###Lembrar de habilitar PHATH para todos users!!!!!###Ф
echo У###                                                ###Ф
echo У######################################################Ф
pause
start python-2.7.14.msi
pause
CLS
echo У######################################################Ф
echo У###                                                ###Ф
echo У###                                                ###Ф
echo У###      Configurando bibliotecas auxiliares       ###Ф
echo У###                                                ###Ф
echo У###                                                ###Ф
echo У######################################################Ф
pip install matplotlib
pip install modbus_tk
pause
CLS
echo У######################################################Ф
echo У###                                                ###Ф
echo У###                                                ###Ф
echo У###               Instalando QT                    ###Ф
echo У###                                                ###Ф
echo У###                                                ###Ф
echo У######################################################Ф
pause
start PyQt4-4.10-gpl-Py2.7-Qt4.8.4-x32.exe
pause
CLS
echo У######################################################Ф
echo У###                                                ###Ф
echo У###         Copiando Arquivos para sistema         ###Ф
echo У###        Selecione a Opзгo D = diretorio         ###Ф
echo У###                                                ###Ф
echo У######################################################Ф
pause
xcopy Sup c:\Sup /E /K
cd \sup
copy Supervisorio.lnk  "%homepath%/desktop/Supervisorio.lnk"
CLS
echo У######################################################Ф
echo У###                                                ###Ф
echo У###                                                ###Ф
echo У###   Parabens seu sistema esta pronto para o uso  ###Ф
echo У###                                                ###Ф
echo У###                                                ###Ф
echo У######################################################Ф
pause


