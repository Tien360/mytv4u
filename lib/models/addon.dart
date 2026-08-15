class AddonManifest {
  final String id;
  final String version;
  final String name;
  final String description;
  final String logo;
  final List<String> types;
  final List<AddonResource> resources;
  final List<AddonCatalog> catalogs;
  final String transportUrl;

  AddonManifest({
    required this.id,
    required this.version,
    required this.name,
    required this.description,
    required this.logo,
    required this.types,
    required this.resources,
    required this.catalogs,
    required this.transportUrl,
  });

  factory AddonManifest.fromJson(Map<String, dynamic> json, String transportUrl) {
    List<AddonResource> parsedResources = [];
    if (json['resources'] != null) {
      for (var r in json['resources']) {
        if (r is String) {
          parsedResources.add(AddonResource(name: r, types: [], idPrefixes: []));
        } else if (r is Map) {
          parsedResources.add(AddonResource.fromJson(r as Map<String, dynamic>));
        }
      }
    }

    List<AddonCatalog> parsedCatalogs = [];
    if (json['catalogs'] != null) {
      for (var c in json['catalogs']) {
        parsedCatalogs.add(AddonCatalog.fromJson(c as Map<String, dynamic>));
      }
    }

    return AddonManifest(
      id: json['id'] ?? '',
      version: json['version'] ?? '',
      name: json['name'] ?? 'Unknown Addon',
      description: json['description'] ?? '',
      logo: json['logo'] ?? '',
      types: List<String>.from(json['types'] ?? []),
      resources: parsedResources,
      catalogs: parsedCatalogs,
      transportUrl: transportUrl,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'version': version,
      'name': name,
      'description': description,
      'logo': logo,
      'types': types,
      'resources': resources.map((r) => r.toJson()).toList(),
      'catalogs': catalogs.map((c) => c.toJson()).toList(),
      'transportUrl': transportUrl,
    };
  }

  /// Returns the base URL for fetching data from this addon.
  /// If transportUrl ends with manifest.json, we strip it.
  String get baseUrl {
    if (transportUrl.endsWith('/manifest.json')) {
      return transportUrl.substring(0, transportUrl.length - 14);
    }
    return transportUrl;
  }
}

class AddonResource {
  final String name;
  final List<String> types;
  final List<String> idPrefixes;

  AddonResource({
    required this.name,
    required this.types,
    required this.idPrefixes,
  });

  factory AddonResource.fromJson(Map<String, dynamic> json) {
    return AddonResource(
      name: json['name'] ?? '',
      types: List<String>.from(json['types'] ?? []),
      idPrefixes: List<String>.from(json['idPrefixes'] ?? []),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'types': types,
      'idPrefixes': idPrefixes,
    };
  }
}

class AddonCatalog {
  final String type;
  final String id;
  final String name;

  AddonCatalog({
    required this.type,
    required this.id,
    required this.name,
  });

  factory AddonCatalog.fromJson(Map<String, dynamic> json) {
    return AddonCatalog(
      type: json['type'] ?? '',
      id: json['id'] ?? '',
      name: json['name'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'type': type,
      'id': id,
      'name': name,
    };
  }
}
