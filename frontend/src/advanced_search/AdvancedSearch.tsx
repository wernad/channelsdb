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
              errors.minRadius = "Min distance must be less than max distance.";
            }

            return errors;
          }}
          onSubmit={async (values, { setSubmitting }) => {
            const ids = await this.fetchIds(values as FilterData);
            this.props.state.fullSearch.onNext(void 0);
            console.log(ids);
            if (ids !== undefined || ids.length > 0) {
              updateViewState(this.props.state, { kind: 'Filter', term: ids });
            } else {
              updateViewState(this.props.state, { kind: 'Info' });
            }
            setSubmitting(false);
          }}
        >
          {({ isSubmitting }) => (
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

                {/* Distance */}
                <div className="col-md-3">
                  <label className="form-label">Distance</label>
                  <Field
                    type="number"
                    min={0}
                    name="minDistance"
                    placeholder="Minimum Distance"
                    className="form-control"
                  />
                  <ErrorMessage name="minDistance" component="div" className="text-danger small" />
                  <Field
                    type="number"
                    min={0}
                    name="maxDistance"
                    placeholder="Maximum Distance"
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
                <div className="col-md-3 flex-column align-items-start align-self-end gap-2 py-4">
                  <div className="w-100 col align-self-start mb-4">
                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className="btn btn-primary mt-7"
                    >
                      Submit
                    </button>
                  </div>
                  <div className="w-100 col align-self-end">
                    <button
                      type="button"
                      className="btn btn-secondary"
                      onClick={() => updateViewState(this.props.state, { kind: "Info" })}
                    >
                      Reset
                    </button>

                  </div>
                </div>
              </div>
            </Form>
          )}
        </Formik>
      </div>
    )
  }
}

{/* <Formik
          initialValues={{ minRadius: "", maxRadius: "", minDistance: "", maxDistance: "", minBottleneck: "" }}
          validate={values => {
            const errors: any = {};
            if (values.maxRadius !== "" && values.minRadius > values.maxRadius) {
              errors.minRadius = "Min radius must be less than max radius."
            }

            return errors;

          }}

          onSubmit={async (values, { setSubmitting }) => {
            const ids = await this.fetchIds(values as FilterData)
            this.props.state.fullSearch.onNext(void 0);
            updateViewState(this.props.state, { kind: 'Filter', term: ids });
          }}
        >
          {({ isSubmitting }) => (
            <Form>
              <div className="row">
                <div className="col-md-4 d-flex flex-col gap-3">
                  <div>
                    <div>
                      <label>Radius</label>
                    </div>
                    <div>
                      <Field label="Min Radius" type="number" min={0} name="minRadius" placeholder="Minimum Radius" />
                      <ErrorMessage name="minRadius" component="div" />
                      <Field type="number" min={0} name="maxRadius" placeholder="Maximum Radius" />
                      <ErrorMessage name="maxRadius" component="div" />
                    </div>
                  </div>
                </div>

                <div className="col-md-4">
                  <div>
                    <div>
                      <label>Distance</label>
                    </div>
                    <div>
                      <Field type="number" min={0} name="minDistance" placeholder="Minimum Distance" />
                      <ErrorMessage name="minDistance" component="div" />
                      <Field type="number" min={0} name="maxDistance" placeholder="Maximum Distance" />
                      <ErrorMessage name="maxDistance" component="div" />
                    </div>

                  </div>
                </div> 


                <div className="col-md-4">

                  <label>Bottleneck</label>
                  <Field type="number" min={0} name="minBottleneck" placeholder="Minimum Bottleneck" />
                  <ErrorMessage name="minBottleneck" component="div" />
                </div>
                
                <div>
                  <button type="submit" disabled={isSubmitting}>
                    Submit
                  </button>
                  <button type="button" disabled={isSubmitting} onClick={() => { updateViewState(this.props.state, { kind: "Info" }) }}>
                    Reset
                  </button>

                </div>
              </div >
            </Form >
          )}

        </Formik > */}