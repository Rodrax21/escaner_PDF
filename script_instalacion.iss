; Script generado para Inno Setup

[Setup]
AppName=PDF Scanner
AppVersion=1.0
DefaultDirName={pf}\PDF Scanner
DefaultGroupName=The R Group
AllowNoIcons=yes
OutputBaseFilename=PDF_Scanner_Installer
OutputDir=Output
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
SetupIconFile=resources\Antodrogas.ico
DisableDirPage=no
DisableProgramGroupPage=yes
ShowLanguageDialog=yes
WizardStyle=modern

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\PDF Scanner v1\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\PDF Scanner"; Filename: "{app}\PDF Scanner v1.exe"; 
Name: "{commondesktop}\PDF Scanner"; Filename: "{app}\PDF Scanner v1.exe"; Tasks: desktopicon; 

[Run]
Filename: "{app}\PDF Scanner v1.exe"; Description: "Ejecutar PDF Scanner"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  DataPath: string;
  UserChoice: Integer;
begin
  if CurUninstallStep = usUninstall then
  begin
    // Preguntar al usuario si desea eliminar la carpeta
    UserChoice := MsgBox('¿Desea eliminar también los datos generados en la carpeta "Documentos\PDF Scanner"?',
                         mbConfirmation, MB_YESNO or MB_DEFBUTTON2);

    if UserChoice = IDYES then
    begin
      DataPath := ExpandConstant('{userdocs}\PDF Scanner');
      DelTree(DataPath, True, True, True);
    end;
  end
end;

