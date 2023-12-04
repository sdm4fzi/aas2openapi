from enum import Enum


class ServiceDescriptionProfilesItem(str, Enum):
    HTTPSADMIN_SHELL_IOAASAPI30AASXFILESERVERSERVICESPECIFICATIONSSP_001 = (
        "https://admin-shell.io/aas/API/3/0/AasxFileServerServiceSpecification/SSP-001"
    )
    HTTPSADMIN_SHELL_IOAASAPI30ASSETADMINISTRATIONSHELLREGISTRYSERVICESPECIFICATIONSSP_001 = (
        "https://admin-shell.io/aas/API/3/0/AssetAdministrationShellRegistryServiceSpecification/SSP-001"
    )
    HTTPSADMIN_SHELL_IOAASAPI30ASSETADMINISTRATIONSHELLREGISTRYSERVICESPECIFICATIONSSP_002 = (
        "https://admin-shell.io/aas/API/3/0/AssetAdministrationShellRegistryServiceSpecification/SSP-002"
    )
    HTTPSADMIN_SHELL_IOAASAPI30ASSETADMINISTRATIONSHELLREPOSITORYSERVICESPECIFICATIONSSP_001 = (
        "https://admin-shell.io/aas/API/3/0/AssetAdministrationShellRepositoryServiceSpecification/SSP-001"
    )
    HTTPSADMIN_SHELL_IOAASAPI30ASSETADMINISTRATIONSHELLREPOSITORYSERVICESPECIFICATIONSSP_002 = (
        "https://admin-shell.io/aas/API/3/0/AssetAdministrationShellRepositoryServiceSpecification/SSP-002"
    )
    HTTPSADMIN_SHELL_IOAASAPI30ASSETADMINISTRATIONSHELLSERVICESPECIFICATIONSSP_001 = (
        "https://admin-shell.io/aas/API/3/0/AssetAdministrationShellServiceSpecification/SSP-001"
    )
    HTTPSADMIN_SHELL_IOAASAPI30ASSETADMINISTRATIONSHELLSERVICESPECIFICATIONSSP_002 = (
        "https://admin-shell.io/aas/API/3/0/AssetAdministrationShellServiceSpecification/SSP-002"
    )
    HTTPSADMIN_SHELL_IOAASAPI30CONCEPTDESCRIPTIONSERVICESPECIFICATIONSSP_001 = (
        "https://admin-shell.io/aas/API/3/0/ConceptDescriptionServiceSpecification/SSP-001"
    )
    HTTPSADMIN_SHELL_IOAASAPI30DISCOVERYSERVICESPECIFICATIONSSP_001 = (
        "https://admin-shell.io/aas/API/3/0/DiscoveryServiceSpecification/SSP-001"
    )
    HTTPSADMIN_SHELL_IOAASAPI30SUBMODELREGISTRYSERVICESPECIFICATIONSSP_001 = (
        "https://admin-shell.io/aas/API/3/0/SubmodelRegistryServiceSpecification/SSP-001"
    )
    HTTPSADMIN_SHELL_IOAASAPI30SUBMODELREGISTRYSERVICESPECIFICATIONSSP_002 = (
        "https://admin-shell.io/aas/API/3/0/SubmodelRegistryServiceSpecification/SSP-002"
    )
    HTTPSADMIN_SHELL_IOAASAPI30SUBMODELREPOSITORYSERVICESPECIFICATIONSSP_001 = (
        "https://admin-shell.io/aas/API/3/0/SubmodelRepositoryServiceSpecification/SSP-001"
    )
    HTTPSADMIN_SHELL_IOAASAPI30SUBMODELREPOSITORYSERVICESPECIFICATIONSSP_002 = (
        "https://admin-shell.io/aas/API/3/0/SubmodelRepositoryServiceSpecification/SSP-002"
    )
    HTTPSADMIN_SHELL_IOAASAPI30SUBMODELREPOSITORYSERVICESPECIFICATIONSSP_003 = (
        "https://admin-shell.io/aas/API/3/0/SubmodelRepositoryServiceSpecification/SSP-003"
    )
    HTTPSADMIN_SHELL_IOAASAPI30SUBMODELREPOSITORYSERVICESPECIFICATIONSSP_004 = (
        "https://admin-shell.io/aas/API/3/0/SubmodelRepositoryServiceSpecification/SSP-004"
    )
    HTTPSADMIN_SHELL_IOAASAPI30SUBMODELSERVICESPECIFICATIONSSP_001 = (
        "https://admin-shell.io/aas/API/3/0/SubmodelServiceSpecification/SSP-001"
    )
    HTTPSADMIN_SHELL_IOAASAPI30SUBMODELSERVICESPECIFICATIONSSP_002 = (
        "https://admin-shell.io/aas/API/3/0/SubmodelServiceSpecification/SSP-002"
    )
    HTTPSADMIN_SHELL_IOAASAPI30SUBMODELSERVICESPECIFICATIONSSP_003 = (
        "https://admin-shell.io/aas/API/3/0/SubmodelServiceSpecification/SSP-003"
    )

    def __str__(self) -> str:
        return str(self.value)
