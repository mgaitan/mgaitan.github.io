<!--
.. title: Ignorando cambios en git localmente
.. slug: ignorando-cambios-en-git-localmente
.. date: 2025-10-31 14:19:23 UTC-03:00
.. tags: git, til, gitignore
.. category:
.. link:
.. description:
.. type: text
-->

Es bien conocido que en un repositorio de git podemos usar un archivo [`.gitignore`](https://git-scm.com/docs/gitignore) para omitir el seguimiento de archivos que no queremos que se suban (se "empujen") al repositorio remoto. Si un archivo coincide con el patrón de un `.gitignore`, entonces no se mostrará en un `git status` para añadir sus eventuales cambios a un commit.

Típicamente se usan para ignorar directorios donde se instalan dependencias (e.g. el virtualenv para proyectos Python generalmente instalado en `.venv`), archivos temporales generados por el intérprete o compilador, archivos específicos para IDEs, etc.

Son tan comunes que GitHub ofrece [plantillas de gitignore](https://github.com/github/gitignore) curadas para distintos lenguajes de programación, y herramientas específicas para inicializar proyectos como [uv init](https://docs.astral.sh/uv/concepts/projects/init/) generan un `.gitignore` básico como parte del *boilerplate*.

Un `.gitignore` forma parte del proyecto (está commiteado) y es importante que esté en el repositorio para que todos los colaboradores tengan la misma configuración.

¿Pero qué pasa si queremos ignorar archivos solo localmente?

<!-- TEASER_END -->


Para eso existen dos maneras:

- `.git/info/exclude` dentro del proyecto, que tiene el mismo formato pero no se versiona en el repositorio y solo afecta al repositorio local.
- `$HOME/.config/git/ignore` cumple la misma función pero afecta a todos los repositorios del usuario.

¿Unos tips extra? Si querés saber todos los archivos ignorados en el repo:

```
git status --ignored
```

Si tenés patrones complejos o varios archivos `.gitignore` a distintos niveles, podés ver qué archivos están siendo ignorados por cuál configuración con:

```
git check-ignore -v <archivo>
```
