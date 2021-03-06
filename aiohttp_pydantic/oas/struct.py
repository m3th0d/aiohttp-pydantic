"""
Utility to write Open Api Specifications using the Python language.
"""

from typing import List, Union


class Info:
    def __init__(self, spec: dict):
        self._spec = spec.setdefault("info", {})

    @property
    def title(self):
        return self._spec.get("title")

    @title.setter
    def title(self, title):
        self._spec["title"] = title

    @property
    def description(self):
        return self._spec.get("description")

    @description.setter
    def description(self, description):
        self._spec["description"] = description

    @property
    def version(self):
        return self._spec.get("version")

    @version.setter
    def version(self, version):
        self._spec["version"] = version

    @property
    def terms_of_service(self):
        return self._spec.get("termsOfService")

    @terms_of_service.setter
    def terms_of_service(self, terms_of_service):
        self._spec["termsOfService"] = terms_of_service


class RequestBody:
    def __init__(self, spec: dict):
        self._spec = spec.setdefault("requestBody", {})

    @property
    def description(self):
        return self._spec["description"]

    @description.setter
    def description(self, description: str):
        self._spec["description"] = description

    @property
    def required(self) -> bool:
        return self._spec.get("required", False)

    @required.setter
    def required(self, required: bool):
        self._spec["required"] = required

    @property
    def content(self):
        return self._spec["content"]

    @content.setter
    def content(self, content: dict):
        self._spec["content"] = content


class Parameter:
    def __init__(self, spec: dict):
        self._spec = spec

    @property
    def name(self) -> str:
        return self._spec["name"]

    @name.setter
    def name(self, name: str):
        self._spec["name"] = name

    @property
    def in_(self) -> str:
        return self._spec["in"]

    @in_.setter
    def in_(self, in_: str):
        self._spec["in"] = in_

    @property
    def description(self) -> str:
        return self._spec["description"]

    @description.setter
    def description(self, description: str):
        self._spec["description"] = description

    @property
    def required(self) -> bool:
        return self._spec["required"]

    @required.setter
    def required(self, required: bool):
        self._spec["required"] = required

    @property
    def schema(self) -> dict:
        return self._spec["schema"]

    @schema.setter
    def schema(self, schema: dict):
        self._spec["schema"] = schema


class Parameters:
    def __init__(self, spec):
        self._spec = spec
        self._spec.setdefault("parameters", [])

    def __getitem__(self, item: int) -> Parameter:
        if item == len(self._spec["parameters"]):
            spec = {}
            self._spec["parameters"].append(spec)
        else:
            spec = self._spec["parameters"][item]
        return Parameter(spec)


class Header:
    def __init__(self, spec: dict, name: str):
        self._spec = spec.setdefault(name, {})
        self._schema = self._spec.setdefault("schema", {})

    @property
    def type_(self) -> str:
        return self._schema["type"]

    @type_.setter
    def type_(self, type_: str):
        self._schema["type"] = type_

    @property
    def example(self) -> str:
        return self._schema["example"]

    @example.setter
    def example(self, example: str):
        self._schema["example"] = example


class Headers:
    def __init__(self, spec: dict):
        self._spec = spec.setdefault("headers", {})

    def __getitem__(self, name: str) -> Header:
        return Header(self._spec, name)


class Response:
    def __init__(self, spec: dict):
        self._spec = spec
        self._spec.setdefault("description", "")

    @property
    def description(self) -> str:
        return self._spec["description"]

    @description.setter
    def description(self, description: str):
        self._spec["description"] = description

    @property
    def content(self):
        return self._spec["content"]

    @content.setter
    def content(self, content: dict):
        self._spec["content"] = content

    @property
    def headers(self) -> Headers:
        return Headers(self._spec)


class Responses:
    def __init__(self, spec: dict):
        self._spec = spec.setdefault("responses", {})

    def __getitem__(self, status_code: Union[int, str]) -> Response:
        if not (100 <= int(status_code) < 600):
            raise ValueError("status_code must be between 100 and 599")

        spec = self._spec.setdefault(str(status_code), {})
        return Response(spec)


class SecurityItem:
    def __init__(self, spec: list):
        self._spec = spec


class Security:
    def __init__(self, spec: dict):
        self._spec = spec.setdefault("security", [])

    def __getitem__(self, item: str) -> SecurityItem:
        existing = [x for x in self._spec if next(iter(x)) == item]
        if existing:
            item_spec = next(iter(existing[0].values()))
        else:
            item_spec = []
            self._spec.append({item: item_spec})
        return SecurityItem(item_spec)


class OperationObject:
    def __init__(self, spec: dict):
        self._spec = spec

    @property
    def summary(self) -> str:
        return self._spec["summary"]

    @summary.setter
    def summary(self, summary: str):
        self._spec["summary"] = summary

    @property
    def description(self) -> str:
        return self._spec["description"]

    @description.setter
    def description(self, description: str):
        self._spec["description"] = description

    @property
    def tags(self) -> List[str]:
        return self._spec["tags"]

    @tags.setter
    def tags(self, tags: List[str]):
        self._spec["tags"] = tags

    @property
    def operation_id(self) -> str:
        return self._spec["operationId"]

    @operation_id.setter
    def operation_id(self, operation_id: str):
        self._spec["operationId"] = operation_id

    @property
    def request_body(self) -> RequestBody:
        return RequestBody(self._spec)

    @property
    def parameters(self) -> Parameters:
        return Parameters(self._spec)

    @property
    def responses(self) -> Responses:
        return Responses(self._spec)

    @property
    def security(self) -> Security:
        return Security(self._spec)


class PathItem:
    def __init__(self, spec: dict):
        self._spec = spec

    @property
    def get(self) -> OperationObject:
        return OperationObject(self._spec.setdefault("get", {}))

    @property
    def put(self) -> OperationObject:
        return OperationObject(self._spec.setdefault("put", {}))

    @property
    def post(self) -> OperationObject:
        return OperationObject(self._spec.setdefault("post", {}))

    @property
    def delete(self) -> OperationObject:
        return OperationObject(self._spec.setdefault("delete", {}))

    @property
    def options(self) -> OperationObject:
        return OperationObject(self._spec.setdefault("options", {}))

    @property
    def head(self) -> OperationObject:
        return OperationObject(self._spec.setdefault("head", {}))

    @property
    def patch(self) -> OperationObject:
        return OperationObject(self._spec.setdefault("patch", {}))

    @property
    def trace(self) -> OperationObject:
        return OperationObject(self._spec.setdefault("trace", {}))

    @property
    def description(self) -> str:
        return self._spec["description"]

    @description.setter
    def description(self, description: str):
        self._spec["description"] = description

    @property
    def summary(self) -> str:
        return self._spec["summary"]

    @summary.setter
    def summary(self, summary: str):
        self._spec["summary"] = summary


class Paths:
    def __init__(self, spec: dict):
        self._spec = spec.setdefault("paths", {})

    def __getitem__(self, path: str) -> PathItem:
        spec = self._spec.setdefault(path, {})
        return PathItem(spec)


class Server:
    def __init__(self, spec: dict):
        self._spec = spec

    @property
    def url(self) -> str:
        return self._spec["url"]

    @url.setter
    def url(self, url: str):
        self._spec["url"] = url

    @property
    def description(self) -> str:
        return self._spec["description"]

    @description.setter
    def description(self, description: str):
        self._spec["description"] = description


class Servers:
    def __init__(self, spec: dict):
        self._spec = spec
        self._spec.setdefault("servers", [])

    def __getitem__(self, item: int) -> Server:
        if item == len(self._spec["servers"]):
            spec = {}
            self._spec["servers"].append(spec)
        else:
            spec = self._spec["servers"][item]
        return Server(spec)


class Components:
    def __init__(self, spec: dict):
        self._spec = spec.setdefault("components", {})

    @property
    def schemas(self) -> dict:
        return self._spec.setdefault("schemas", {})

    @property
    def security_schemes(self) -> dict:
        return self._spec.setdefault("securitySchemes", {})


class OpenApiSpec3:
    def __init__(self):
        self._spec = {"openapi": "3.0.0"}

    @property
    def info(self) -> Info:
        return Info(self._spec)

    @property
    def servers(self) -> Servers:
        return Servers(self._spec)

    @property
    def paths(self) -> Paths:
        return Paths(self._spec)

    @property
    def components(self) -> Components:
        return Components(self._spec)

    @property
    def spec(self):
        return self._spec
