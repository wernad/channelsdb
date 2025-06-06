import * as React from "react";
import { Formik, Form, Field, ErrorMessage } from 'formik';
import { fetchFilter, FilterData, State, updateViewState } from "../State";




export class AdvancedSearch extends React.Component<{ state: State }, FilterData> {
  private fetchIds = async (data: FilterData) => {
    try {
      const url = this.props.state.channelsUrl;
      const ids = await fetchFilter(this.props.state, data);
      return ids;
    } catch (e) {
      if (e === "Not Found") {
        return [];
      }
    }
  }

  render() {
    return (
      <div className="form-group form-group-lg container">
        <Formik
          initialValues={{ minRadius: "", maxRadius: "", minDistance: "", maxDistance: "", minBottleneck: "" }}
          validate={values => {
            const errors: any = {};
            if (values.maxRadius !== "" && values.minRadius > values.maxRadius) {
              errors.minRadius = "Min radius must be less than max radius.";
            }

            if (values.maxDistance !== "" && values.minDistance > values.maxDistance) {
              errors.minRadius = "Min Length must be less than max Length.";
            }

            return errors;
          }}
          onSubmit={async (values, { setSubmitting }) => {
            const ids = await this.fetchIds(values as FilterData);
            this.props.state.fullSearch.onNext(void 0);
            if (ids !== undefined) {
              updateViewState(this.props.state, { kind: 'Info' }); // Reset entries.
              updateViewState(this.props.state, { kind: 'Filter', term: ids });
            } else {
              updateViewState(this.props.state, { kind: 'Info' });
            }
            setSubmitting(false);
          }}
        >
          {(formik) => (
            <Form>
              <div className="row g-4 align-items-end">
                {/* Radius */}
                <div className="col-md-3">
                  <label className="form-label">Radius</label>
                  <Field
                    type="number"
                    min={0}
                    name="minRadius"
                    placeholder="Minimum Radius"
                    className="form-control"
                  />
                  <ErrorMessage name="minRadius" component="div" className="text-danger small" />
                  <Field
                    type="number"
                    min={0}
                    name="maxRadius"
                    placeholder="Maximum Radius"
                    className="form-control mt-2"
                  />
                  <ErrorMessage name="maxRadius" component="div" className="text-danger small" />
                </div>

                {/* Length */}
                <div className="col-md-3">
                  <label className="form-label">Length</label>
                  <Field
                    type="number"
                    min={0}
                    name="minDistance"
                    placeholder="Minimum Length"
                    className="form-control"
                  />
                  <ErrorMessage name="minDistance" component="div" className="text-danger small" />
                  <Field
                    type="number"
                    min={0}
                    name="maxDistance"
                    placeholder="Maximum Length"
                    className="form-control mt-2"
                  />
                  <ErrorMessage name="maxDistance" component="div" className="text-danger small" />
                </div>

                {/* Bottleneck */}
                <div className="col-md-3">
                  <label className="form-label">Bottleneck</label>
                  <Field
                    type="number"
                    min={0}
                    name="minBottleneck"
                    placeholder="Minimum Bottleneck"
                    className="form-control"
                  />
                  <ErrorMessage name="minBottleneck" component="div" className="text-danger small" />
                </div>

                {/* Buttons */}
                <div className="ol-md-3 d-flex flex-column justify-content-center align-items-center h-100">
                  <button
                    type="submit"
                    disabled={formik.isSubmitting}
                    className="btn btn-primary mb-4 w-75"
                  >
                    Submit
                  </button>
                  <button
                    type="button"
                    className="btn btn-secondary w-75"
                    onClick={() => {
                      formik.resetForm();
                      updateViewState(this.props.state, { kind: "Info" }
                      )
                    }}
                  >
                    Reset
                  </button>
                </div>
              </div>
            </Form>
          )}
        </Formik>
      </div>
    )
  }
}
