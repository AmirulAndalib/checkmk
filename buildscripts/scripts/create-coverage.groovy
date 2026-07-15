#!groovy

/// file: create-coverage.groovy

void main() {
    def test_jenkins_helper = load("${checkout_dir}/buildscripts/scripts/utils/test_helper.groovy");
    def versioning = load("${checkout_dir}/buildscripts/scripts/utils/versioning.groovy");

    def safe_branch_name = versioning.safe_branch_name();
    def container_safe_branch_name = safe_branch_name.replace(".", "-");

    dir("${checkout_dir}") {
        withCredentials([
            string(credentialsId: "CI_TEST_SQL_DB_ENDPOINT", variable: "CI_TEST_SQL_DB_ENDPOINT"),
            usernamePassword(
                credentialsId: 'qa-kpi-metabase-postgres',
                usernameVariable: 'QA_POSTGRES_USER',
                passwordVariable: 'QA_POSTGRES_PASSWORD'
            ),
        ]) {
            test_jenkins_helper.execute_test([
                name: "create-coverage",
                cmd: """\
export POSTGRES_HOST="dev-kpi.lan.checkmk.net"
export POSTGRES_PORT=5432
export POSTGRES_DB=metabase
tests/qa_metrics/test_coverage/main.sh --run --upload-totals --upload-per-module""",
                container_name: "ubuntu-2404-${container_safe_branch_name}-latest",
                disable_hot_cache: true,
            ]);
        }
    }
}

return this;
