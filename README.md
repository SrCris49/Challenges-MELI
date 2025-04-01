%%{init: {'theme': 'neutral', 'fontFamily': 'Arial', 'gantt': {'barHeight': 20}}}%%
flowchart TD
    %% Nodos principales
    A[["Arquitectura Segura<br>(5 Pilares Fundamentales)"]] 
    style A fill:#2ecc71,stroke:#27ae60,color:white,stroke-width:2px
    
    %% Pilar 1 - Autenticación
    B[["<b>1. Autenticación Fortalecida</b><br>• MFA Obligatorio<br>• IAM con Roles AWS/GCP<br>• Certificados Digitales"]]
    style B fill:#3498db,stroke:#2980b9
    
    %% Pilar 2 - Protección Datos
    C[["<b>2. Protección de Datos</b><br>• Encriptación AES-256/E2E<br>• Tokenización<br>• Anonimización"]]
    style C fill:#9b59b6,stroke:#8e44ad
    
    %% Pilar 3 - Monitorización
    D[["<b>3. Monitorización Inteligente</b><br>• SIEM con Elastic/SPLUNK<br>• Detección Anomalías ML<br>• Scoring Automático"]]
    style D fill:#e67e22,stroke:#d35400
    
    %% Pilar 4 - Resiliencia
    E[["<b>4. Resiliencia Operacional</b><br>• Backups 3-2-1<br>• DRP Automatizado<br>• Clusterización"]]
    style E fill:#1abc9c,stroke:#16a085
    
    %% Pilar 5 - Cumplimiento
    F[["<b>5. Cumplimiento Normativo</b><br>• Auditorías Continuas<br>• GDPR/HIPAA/ISO27001<br>• Policy as Code"]]
    style F fill:#f1c40f,stroke:#f39c12
    
    %% Relaciones y flujo
    A --> B & C & D & E & F
    
    %% Subsistemas
    B --> G[["<b>Control de Accesos</b><br>• RBAC/ABAC<br>• Least Privilege<br>• JIT Access"]]
    C --> H[["<b>Cifrado</b><br>• TLS 1.3+<br>• HSM<br>• Key Rotation"]]
    D --> I[["<b>Respuesta Automatizada</b><br>• Playbooks SOAR<br>• Cuarentena Automática<br>• Threat Intelligence"]]
    
    %% Elemento diferenciador
    D --> J[["<b>SISTEMA DE SCORING</b><br>▸ Nivel de Riesgo por Componente<br>▸ Priorización Automática<br>▸ Integración NIST CSF"]]
    style J fill:#e74c3c,stroke:#c0392b,color:white
    
    %% Leyenda
    subgraph Leyenda
        X[Pilar Fundamental] --> Y[Subsistema]
        style X fill:#ecf0f1,stroke:#bdc3c7
        style Y fill:#ecf0f1,stroke:#bdc3c7
    end
