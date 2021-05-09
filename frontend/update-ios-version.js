/* eslint-disable @typescript-eslint/no-var-requires */
const xcode = require("xcode");
const fs = require("fs");
const pkg = require("./package.json");

const projectPath = "src-capacitor/ios/App/App.xcodeproj/project.pbxproj";
const project = xcode.project(projectPath);

project.parse(() => {
  const currentProjectVersion = project.getBuildProperty(
    "CURRENT_PROJECT_VERSION",
    "Release",
    "App",
  );

  const newProjectVersion = currentProjectVersion + 1;
  const newMarketingVersion = pkg.version;

  for (const build of ["Debug", "Release"]) {
    project.updateBuildProperty(
      "CURRENT_PROJECT_VERSION",
      newProjectVersion,
      build,
      "App",
    );

    project.updateBuildProperty(
      "MARKETING_VERSION",
      newMarketingVersion,
      build,
      "App",
    );
  }

  fs.writeFileSync(projectPath, project.writeSync());
});
